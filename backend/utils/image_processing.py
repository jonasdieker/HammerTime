import json
import base64
from pathlib import Path
import anthropic
import csv
import yaml
import request_agent as ra 


with open("secrets.yaml", "r", encoding="utf-8") as f:
    secrets = yaml.safe_load(f)


def describe_construction_site_image(image_path: str, additional_context: str = "") -> dict:
    """
    Analyze an image from a construction/procurement perspective.
    Returns a foreman-style description of what's needed.
    
    Args:
        image_path: Path to the image file
        additional_context: Optional additional context about the site/task
    
    Returns:
        dict with 'description', 'tasks_identified', 'materials_needed', 'safety_concerns'
    """
    
    # Resolve Anthropic API key
    api_key = secrets.get('API_KEY')
    client = anthropic.Anthropic(api_key=api_key)
    
    # Read and encode the image
    with open(image_path, "rb") as image_file:
        image_data = base64.standard_b64encode(image_file.read()).decode("utf-8")
    
    # Determine media type from file extension
    extension = Path(image_path).suffix.lower()
    media_types = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.webp': 'image/webp'
    }
    media_type = media_types.get(extension, 'image/jpeg')
    
    # Build context string
    context_part = f"\n\nAdditional site context: {additional_context}" if additional_context else ""
    
    # Create foreman-focused prompt
    prompt = f"""You are an experienced construction site worker analyzing this image for procurement and work planning.

    Analyze the construction site items (only the ones in the FOCUS OF THE IMAGE) in the image like a would and provide a detailed description for ordering the depicted product(s) in the image

    {context_part}

    Be thorough but concise. Think like you're writing a shopping list team.

    RETURN: A precise, concise procurement list of the items detected in the given context, LESS is MORE"""

    # Call Claude API with image
    print("Analyzing construction site image...")
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_data,
                        },
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ],
            }
        ],
    )

    # Extract a simple text string from the response
    response_text = None
    try:
        response_text = message.content[0].text
    except Exception:
        try:
            response_text = message.content
        except Exception:
            response_text = str(message)

    if not isinstance(response_text, str):
        try:
            response_text = json.dumps(response_text, ensure_ascii=False)
        except Exception:
            response_text = str(response_text)

    return response_text.strip()


def send_description_to_request_agent(description: str, catalog_path: str = 'backend/data/sample.csv') -> dict:
    """
    Send a plain description string into the request agent and return the detailed JSON result.

    - Loads the catalog from `catalog_path` (CSV) if present and strips unwanted fields.
    - Calls `process_procurement_request` from `backend.utils.request_agent`.

    Returns the dict result returned by the request agent (detailed JSON).
    """

    # load catalog
    catalog = []
    try:
        with open(catalog_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('preis_eur'):
                    try:
                        row['preis_eur'] = float(row['preis_eur'])
                    except Exception:
                        pass
                for _k in ('verbrauchsart', 'gefahrgut', 'gefahrengut', 'lagerort'):
                    row.pop(_k, None)
                catalog.append(row)
    except FileNotFoundError:
        catalog = []

    # import process function from request agent (relative if possible

    return ra.process_procurement_request(foreman_message=description, c_materials_data=catalog)


# Example usage
if __name__ == "__main__":
    # Analyze a construction site image
    image_path = "testFiles/image3.png"
    
    # Get a simple foreman-style description string
    description = describe_construction_site_image(
        image_path=image_path,
        additional_context=""
    )

    # Output only a simple string
    print(description)
    print(send_description_to_request_agent(description))