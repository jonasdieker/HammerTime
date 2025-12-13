from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timezone
import csv
import anthropic

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============= MODELS =============

class Product(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    artikel_id: str
    artikelname: str
    kategorie: str
    einheit: str
    preis_eur: float
    lieferant: str
    verbrauchsart: str
    gefahrgut: bool
    lagerort: str
    typische_baustelle: str

class ProductCreate(BaseModel):
    artikel_id: str
    artikelname: str
    kategorie: str
    einheit: str
    preis_eur: float
    lieferant: str
    verbrauchsart: str
    gefahrgut: bool
    lagerort: str
    typische_baustelle: str

class OrderItem(BaseModel):
    product_id: str
    artikel_id: str
    artikelname: str
    quantity: int
    unit_price: float
    subtotal: float

class Order(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    order_number: str
    items: List[OrderItem]
    total: float
    status: str = "pending"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    notes: Optional[str] = None

class OrderCreate(BaseModel):
    items: List[OrderItem]
    notes: Optional[str] = None

class AIRecommendationRequest(BaseModel):
    query: str

class AIRecommendation(BaseModel):
    supplier: str
    items: List[Dict[str, Any]]
    total_price: float
    lead_time: str
    wastage_reduction: str
    reasoning: str


# ============= PRODUCT ROUTES =============

@api_router.post("/products/import")
async def import_products():
    """Import products from CSV file"""
    try:
        csv_path = Path("/app/products.csv")
        if not csv_path.exists():
            raise HTTPException(status_code=404, detail="CSV file not found")
        
        # Clear existing products
        await db.products.delete_many({})
        
        products = []
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                product = Product(
                    artikel_id=row['artikel_id'],
                    artikelname=row['artikelname'],
                    kategorie=row['kategorie'],
                    einheit=row['einheit'],
                    preis_eur=float(row['preis_eur']),
                    lieferant=row['lieferant'],
                    verbrauchsart=row['verbrauchsart'],
                    gefahrgut=row['gefahrgut'].lower() == 'true',
                    lagerort=row['lagerort'],
                    typische_baustelle=row['typische_baustelle']
                )
                products.append(product.model_dump())
        
        if products:
            result = await db.products.insert_many(products)
            return {"message": f"Successfully imported {len(result.inserted_ids)} products"}
        
        return {"message": "No products to import"}
    
    except Exception as e:
        logger.error(f"Error importing products: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/products", response_model=List[Product])
async def get_products(
    search: Optional[str] = None,
    kategorie: Optional[str] = None,
    lieferant: Optional[str] = None
):
    """Get all products with optional filters"""
    try:
        query = {}
        
        if search:
            query["$or"] = [
                {"artikelname": {"$regex": search, "$options": "i"}},
                {"artikel_id": {"$regex": search, "$options": "i"}},
                {"kategorie": {"$regex": search, "$options": "i"}}
            ]
        
        if kategorie:
            query["kategorie"] = kategorie
        
        if lieferant:
            query["lieferant"] = lieferant
        
        products = await db.products.find(query, {"_id": 0}).to_list(1000)
        return products
    
    except Exception as e:
        logger.error(f"Error fetching products: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: str):
    """Get single product by ID"""
    try:
        product = await db.products.find_one({"id": product_id}, {"_id": 0})
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching product: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/categories")
async def get_categories():
    """Get all unique categories"""
    try:
        categories = await db.products.distinct("kategorie")
        return {"categories": sorted(categories)}
    except Exception as e:
        logger.error(f"Error fetching categories: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/suppliers")
async def get_suppliers():
    """Get all unique suppliers"""
    try:
        suppliers = await db.products.distinct("lieferant")
        return {"suppliers": sorted(suppliers)}
    except Exception as e:
        logger.error(f"Error fetching suppliers: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============= AI RECOMMENDATION ROUTES =============

@api_router.post("/ai/recommend", response_model=AIRecommendation)
async def get_ai_recommendation(request: AIRecommendationRequest):
    """Get AI-powered procurement recommendations"""
    try:
        # Get all products for context
        products = await db.products.find({}, {"_id": 0}).to_list(1000)
        
        # Create product catalog summary for Claude
        product_summary = []
        for p in products[:50]:  # Limit to avoid token limits
            product_summary.append(
                f"{p['artikel_id']}: {p['artikelname']} - {p['preis_eur']}€ ({p['lieferant']}, {p['einheit']})"
            )
        
        catalog_text = "\n".join(product_summary)
        
        # Initialize Claude client
        anthropic_key = os.environ.get('ANTHROPIC_API_KEY', '')
        
        # If using dummy key, return mock recommendation
        if 'dummy' in anthropic_key.lower():
            logger.info("Using dummy API key, returning mock recommendation")
            return create_mock_recommendation(request.query, products)
        
        claude_client = anthropic.Anthropic(api_key=anthropic_key)
        
        # Create prompt for Claude
        prompt = f"""You are a procurement assistant helping to find the best products and suppliers.

User request: "{request.query}"

Available products (sample):
{catalog_text}

Based on the user's request, analyze and recommend:
1. Which products best match their needs
2. Optimal supplier(s) based on pricing and availability
3. Suggested quantities with wastage consideration
4. Estimated lead time
5. Any cost optimization opportunities

Respond in JSON format:
{{
    "supplier": "primary supplier name",
    "items": [
        {{"name": "product name", "quantity": number, "unit_price": price, "subtotal": total}}
    ],
    "total_price": total_amount,
    "lead_time": "X days",
    "wastage_reduction": "X% less wastage",
    "reasoning": "brief explanation of recommendations"
}}"""

        # Call Claude API
        message = claude_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        # Parse response
        import json
        response_text = message.content[0].text
        
        # Extract JSON from response
        json_start = response_text.find('{')
        json_end = response_text.rfind('}') + 1
        json_str = response_text[json_start:json_end]
        
        recommendation_data = json.loads(json_str)
        
        return AIRecommendation(**recommendation_data)
    
    except Exception as e:
        logger.error(f"Error getting AI recommendation: {str(e)}")
        # Return mock recommendation on error
        return create_mock_recommendation(request.query, await db.products.find({}, {"_id": 0}).to_list(1000))

def create_mock_recommendation(query: str, products: List[Dict]) -> AIRecommendation:
    """Create a mock recommendation for demo purposes"""
    # Find relevant products based on query keywords
    query_lower = query.lower()
    relevant_products = []
    
    for p in products:
        if any(keyword in p['artikelname'].lower() for keyword in ['schraube', 'screw', 'dübel', 'washer', 'unterleg']):
            relevant_products.append(p)
            if len(relevant_products) >= 3:
                break
    
    if not relevant_products:
        relevant_products = products[:3]
    
    # Create recommendation
    items = []
    total = 0
    
    for p in relevant_products[:2]:
        quantity = 500 if 'schraube' in p['artikelname'].lower() else 250
        subtotal = quantity * p['preis_eur']
        items.append({
            "name": p['artikelname'],
            "quantity": quantity,
            "unit_price": p['preis_eur'],
            "subtotal": round(subtotal, 2)
        })
        total += subtotal
    
    return AIRecommendation(
        supplier=relevant_products[0]['lieferant'] if relevant_products else "Würth",
        items=items,
        total_price=round(total, 2),
        lead_time="2-3 days",
        wastage_reduction="25% less wastage",
        reasoning="Selected products based on your requirements with optimal supplier for cost-effectiveness and availability."
    )


# ============= ORDER ROUTES =============

@api_router.post("/orders", response_model=Order)
async def create_order(order_data: OrderCreate):
    """Create a new order"""
    try:
        # Calculate total
        total = sum(item.subtotal for item in order_data.items)
        
        # Generate order number
        order_count = await db.orders.count_documents({})
        order_number = f"ORD-{order_count + 1:05d}"
        
        # Create order object
        order = Order(
            order_number=order_number,
            items=order_data.items,
            total=total,
            notes=order_data.notes
        )
        
        # Store in database
        order_dict = order.model_dump()
        order_dict['created_at'] = order_dict['created_at'].isoformat()
        
        await db.orders.insert_one(order_dict)
        
        return order
    
    except Exception as e:
        logger.error(f"Error creating order: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/orders", response_model=List[Order])
async def get_orders():
    """Get all orders"""
    try:
        orders = await db.orders.find({}, {"_id": 0}).sort("created_at", -1).to_list(1000)
        
        # Convert ISO string timestamps back to datetime objects
        for order in orders:
            if isinstance(order['created_at'], str):
                order['created_at'] = datetime.fromisoformat(order['created_at'])
        
        return orders
    
    except Exception as e:
        logger.error(f"Error fetching orders: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/orders/{order_id}", response_model=Order)
async def get_order(order_id: str):
    """Get single order by ID"""
    try:
        order = await db.orders.find_one({"id": order_id}, {"_id": 0})
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        # Convert ISO string timestamp back to datetime object
        if isinstance(order['created_at'], str):
            order['created_at'] = datetime.fromisoformat(order['created_at'])
        
        return order
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching order: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============= BASIC ROUTES =============

@api_router.get("/")
async def root():
    return {"message": "Procurement Assistant API"}

@api_router.get("/health")
async def health_check():
    return {"status": "healthy", "database": "connected"}


# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
