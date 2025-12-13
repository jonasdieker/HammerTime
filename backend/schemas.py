# schemas.py
from pydantic import BaseModel

class ProcurementRequest(BaseModel):
    query: str
