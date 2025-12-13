import json
import csv
import os
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
    api_key = None
    try:
        api_key = secrets.get('API_KEY')
    except Exception:
        api_key = None
    if not api_key:
        api_key = os.environ.get('API_KEY')
    if not api_key:
        raise RuntimeError(
            "Anthropic API key not found. Set 'API_KEY' in secrets.yaml or export API_KEY in your environment."
        )

    client = anthropic.Anthropic(api_key=api_key)
    
    # Convert materials data to formatted string
    materials_json = json.dumps(c_materials_data, ensure_ascii=False, indent=2)
    
    # Create the prompt
    prompt = f"""You are a procurement helper tool for onsite C material procurement. 

    Here is the available C-materials catalog:
    {materials_json}

    Based on the foreman's task below, determine which products and quantities are needed.

    Foreman's task: "{foreman_message}"

    
    Return ONLY JSON object with EXACTLY this structure:
    {{
    "materials": [
        ["artikel_id", anzahl],
        ["artikel_id", anzahl]
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
    
    return result


# Example usage
if __name__ == "__main__":
    # Load your C-materials catalog (CSV -> list[dict])
    with open('backend/data/sample.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        c_materials = []
        for row in reader:
            # convert numeric and boolean-like fields
            if row.get('preis_eur'):
                try:
                    row['preis_eur'] = float(row['preis_eur'])
                except ValueError:
                    pass
            g = row.get('gefahrgut', '').strip().lower()
            row['gefahrgut'] = True if g in ('true', '1', 'yes') else False
            c_materials.append(row)
    
    # Example foreman request
    foreman_request = "Building up dry wall order all necessary tools"
    
    # Process the request
    result = process_procurement_request(
        foreman_message=foreman_request,
        c_materials_data=c_materials
    )
    
    # Print results
    print("Procurement Order:")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # Save to file
    with open('procurement_order.json', 'w', encoding='utf-8') as f:
        json.dump(result['materials'], f, ensure_ascii=False, indent=2)
    
    print("\nOrder saved to procurement_order.json")