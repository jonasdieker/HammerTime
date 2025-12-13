from fastapi import FastAPI
from pydantic import BaseModel
from backend.utils.request_agent import process_procurement_request
import csv

app = FastAPI()

# Mock data
MOCK_PARTS = [
    {
        "id": "P001",
        "part_name": "Work Gloves",
        "quantity": 150,
        "suppliers": ["Supplier A", "Supplier B"]
    },
    {
        "id": "P002",
        "part_name": "Wood Screws (Box of 100)",
        "quantity": 75,
        "suppliers": ["Supplier C", "Supplier D", "Supplier E"]
    },
    {
        "id": "P003",
        "part_name": "Safety Goggles",
        "quantity": 200,
        "suppliers": ["Supplier A", "Supplier F"]
    }
]

class PromptRequest(BaseModel):
    prompt: str


# data parsed once at startup
def parse_data():
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
    
    return c_materials

c_materials_catalog = parse_data()
print(c_materials_catalog[:2])


@app.post("/receive_user_prompt")
async def receive_user_prompt(request: PromptRequest):
    """Receives user prompt and returns list of parts with suppliers"""
    suggested_materials = process_procurement_request(request.prompt, c_materials_catalog)
    #TODO: validate IDs are legit
    return suggested_materials


@app.post("/send_foreman_approval")
async def send_foreman_approval(approval_data: dict):
    """Handles foreman approval button click."""
    return {"status": "approved", "message": "Foreman approval recorded"}


@app.get("/approval_list/foreman")
async def get_foreman_approvals():
    """Returns list of foreman-approved items to show in the UI for the procurement team."""
    return MOCK_PARTS


@app.post("/procurement_approval")
async def procurement_approval(approval_data: dict):
    """Handles procurement team approval button click."""
    return {"status": "approved", "message": "Procurement approval recorded"}


@app.get("/approval_list/procurement")
async def get_procurement_approvals():
    """Returns list of procurement-approved items."""
    return MOCK_PARTS


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "HammerTime API is running"}


if __name__ == "__main__":
    import uvicorn
    # Run with: python -m backend.main
    # Or: uvicorn backend.main:app --reload
    uvicorn.run(app, host="0.0.0.0", port=8000)
