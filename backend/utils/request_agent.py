import json
import csv
import difflib
import anthropic
import yaml


with open("secrets.yaml", "r", encoding="utf-8") as f:
    secrets = yaml.safe_load(f)

def process_procurement_request(foreman_message: str, c_materials_data: list) -> dict:
    """
    Process a foreman's procurement request and return necessary C-materials.
    
    Args:
        foreman_message: The foreman's task description
        c_materials_data: List of available C-materials (JSON data)
    
    Returns:
        dict with 'materials' (list of [artikel_id, anzahl]) and 'explanation'
    """
    
    # Resolve Anthropic API key from secrets.yaml or environment
    api_key = secrets.get('API_KEY')

    client = anthropic.Anthropic(api_key=api_key)
    
    materials_json = json.dumps(c_materials_data, ensure_ascii=False, indent=2)
    
    prompt = f"""You are a procurement helper tool for onsite C material procurement. 

    Here is the available C-materials catalog:
    {materials_json}

    Based on the foreman's task below, determine which products and quantities are needed. Order ONLY the absolutely necessary and requested products for the request. 
    Get the BEST deals and try to stay with as few suppliers as possible

    Foreman's task: "{foreman_message}"

    
    RETURN: ONLY JSON object with EXACTLY this structure:
    {{
    "materials": [
        ["artikel_id", anzahl],
        ["artikel_id", anzahl],
        ...
    ],
    "explanation": "Brief explanation of what was ordered and why"
    }}

    Consider:
    - Typical quantities needed for the task
    - All necessary tools, fasteners, and consumables
    - Required PPE (Personal Protective Equipment)
    - Cleaning and preparation materials
    - Consider the task type and select appropriate materials"""

    # Call Claude API
    print("prompting...")
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    print("Raw Response: ", message)
    
    # Extract response
    response_text = message.content[0].text
    
    # Parse JSON response (handle potential markdown code blocks or surrounding text)
    response_text = response_text.strip()

    # Prefer an explicit ```json block, then any ``` block
    start = None
    idx_json = response_text.find("```json")
    idx_code = response_text.find("```")
    if idx_json != -1:
        start = idx_json + len("```json")
    elif idx_code != -1:
        start = idx_code + 3

    if start is not None:
        # look for a closing fence after the start
        end = response_text.find("```", start)
        if end != -1:
            response_text = response_text[start:end].strip()
        else:
            # no closing fence, take the rest
            response_text = response_text[start:].strip()
    else:
        # no code fences found — try to extract a JSON object from the text
        first_brace = response_text.find("{")
        last_brace = response_text.rfind("}")
        if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
            response_text = response_text[first_brace:last_brace+1].strip()

    # final cleanup of any remaining backticks or surrounding whitespace
    if response_text.startswith("```"):
        response_text = response_text[3:].strip()
    if response_text.endswith("```"):
        response_text = response_text[:-3].strip()
    
    result = json.loads(response_text)

    # Enrich/match and price using the provided c_materials_data (avoid re-reading CSV)
    detailed = match_and_price(result, catalog=c_materials_data, approval_threshold=500.0)
    detailed_output = {
        'explanation': result.get('explanation', ''),
        **detailed,
    }

    return detailed_output


def match_and_price(result_json: dict, csv_path: str = 'backend/data/sample.csv', approval_threshold: float = 500.0, catalog: list = None) -> dict:
    """
    Match product IDs from `result_json` to the CSV data, calculate per-item and total prices,
    and set `requireApproval` if total exceeds `approval_threshold`.

    - tolerant matching using exact match (normalized) then fuzzy matching via difflib.
    - missing products tolerated: included with price 0 and matched=False.

    Returns a dict: {"total": float, "requireApproval": bool, "items": [ ... ]}
    """

    # build map from provided catalog (list of dicts) or from CSV file
    material_map = {}
    if catalog:
        for row in catalog:
            key = str(row.get('artikel_id', '')).strip().upper()
            if not key:
                continue
            try:
                row_price = float(row.get('preis_eur') or 0)
            except Exception:
                row_price = 0.0
            # copy row to avoid mutating original
            r = dict(row)
            r['preis_eur'] = row_price
            material_map[key] = r
    else:
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    key = row.get('artikel_id', '').strip().upper()
                    if not key:
                        continue
                    # normalize numeric price
                    try:
                        row['preis_eur'] = float(row.get('preis_eur') or 0)
                    except Exception:
                        row['preis_eur'] = 0.0
                    material_map[key] = row
        except FileNotFoundError:
            material_map = {}

    items_out = []
    total = 0.0

    materials = result_json.get('materials') if isinstance(result_json, dict) else None
    if not materials:
        return {"total": 0.0, "requireApproval": False, "items": []}

    available_keys = list(material_map.keys())

    for entry in materials:
        try:
            artikel_id_raw, anzahl_raw = entry[0], entry[1]
        except Exception:
            # unexpected entry shape; skip
            continue

        artikel_id = str(artikel_id_raw).strip()
        key = artikel_id.upper()

        # parse amount
        try:
            anzahl = int(anzahl_raw)
        except Exception:
            try:
                anzahl = int(float(str(anzahl_raw)))
            except Exception:
                anzahl = 0

        matched = False
        product = material_map.get(key)

        if not product and available_keys:
            # try fuzzy match
            close = difflib.get_close_matches(key, available_keys, n=1, cutoff=0.6)
            if close:
                product = material_map.get(close[0])
                matched = True

        if product:
            preis_stk = float(product.get('preis_eur') or 0.0)
            preis_gesamt = round(anzahl * preis_stk, 2)
            total += preis_gesamt

            item = {
                'artikel_id': product.get('artikel_id', artikel_id),
                'artikelname': product.get('artikelname', ''),
                'kategorie': product.get('kategorie', ''),
                'einheit': product.get('einheit', ''),
                'anzahl': anzahl,
                'preis_stk': preis_stk,
                'preis_gesamt': preis_gesamt,
                'lieferant': product.get('lieferant', ''),
                'typische_baustelle': product.get('typische_baustelle', ''),
                'matched': True,
            }
        else:
            # unknown product, include minimal info
            item = {
                'artikel_id': artikel_id,
                'artikelname': '',
                'kategorie': '',
                'einheit': '',
                'anzahl': anzahl,
                'preis_stk': 0.0,
                'preis_gesamt': 0.0,
                'lieferant': '',
                'typische_baustelle': '',
                'matched': False,
            }

        items_out.append(item)

    total = round(total, 2)
    require_approval = total > float(approval_threshold)

    return {"total": total, "requireApproval": require_approval, "items": items_out}

def clean_voice_transcript(raw_text: str) -> str:
    """
    Uses Claude to clean up raw voice-to-text input, removing filler words
    and extracting the core intent.
    """
    api_key = secrets.get('API_KEY')
    client = anthropic.Anthropic(api_key=api_key)

    prompt = f"""You are a helpful assistant. Clean up this raw voice transcription for a construction procurement app. 
    Remove filler words (um, uh, like), greetings, and politeness markers. 
    Keep only the specific items, quantities, and descriptions needed for the order.
    
    Raw Input: "{raw_text}"
    
    RETURN: ONLY the cleaned text string. Do not add quotes."""

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        # Extract text safely
        if hasattr(message.content[0], 'text'):
            cleaned_text = message.content[0].text.strip()
        else:
            cleaned_text = str(message.content[0]).strip()
        return cleaned_text
    except Exception as e:
        print(f"Error cleaning text: {e}")
        return raw_text

# Example usage
if __name__ == "__main__":
    # Load your C-materials catalog (CSV -> list[dict])
    with open('backend/data/sample.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        c_materials = []
        for row in reader:
            # convert numeric fields
            if row.get('preis_eur'):
                try:
                    row['preis_eur'] = float(row['preis_eur'])
                except ValueError:
                    pass

            # normalize hazard flag if present (don't keep it)
            g = row.get('gefahrgut', row.get('gefahrengut', '')).strip().lower()
            _ = True if g in ('true', '1', 'yes') else False

            # remove unwanted fields from the row
            for _k in ('verbrauchsart', 'gefahrgut', 'gefahrengut', 'lagerort'):
                row.pop(_k, None)

            c_materials.append(row)
    
    # Example foreman request
    foreman_request = "gloves (42069x) and a bucket."
    
    # Process the request (returns detailed output including explanation, total, requireApproval, items)
    detailed_result = process_procurement_request(
        foreman_message=foreman_request,
        c_materials_data=c_materials
    )

    # Print results
    print("Procurement Order (detailed):")
    print(json.dumps(detailed_result, ensure_ascii=False, indent=2))

    # Save a compact order list (artikel_id + anzahl)
    compact = [{'artikel_id': it['artikel_id'], 'anzahl': it['anzahl']} for it in detailed_result.get('items', [])]
    with open('procurement_order.json', 'w', encoding='utf-8') as f:
        json.dump(compact, f, ensure_ascii=False, indent=2)

    # Save the detailed output
    with open('procurement_order_detailed.json', 'w', encoding='utf-8') as f:
        json.dump(detailed_result, f, ensure_ascii=False, indent=2)

    print(detailed_result)

    print("Detailed order saved to procurement_order_detailed.json")