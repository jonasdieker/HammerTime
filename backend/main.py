from langchain_core.messages import HumanMessage

from backend.schemas import ProcurementRequest
from backend.app import app, graph

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


@app.post("/receive_user_prompt")
async def receive_user_prompt(req: ProcurementRequest):
    """Receives user prompt and returns list of parts with suppliers"""
    initial_state = {
        "messages": [HumanMessage(content=req.query)]
    }

    final_state = graph.invoke(initial_state)

    return {
        "result": final_state["messages"][-1].content
    }


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
