from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict
from main import DataGenerator
import uvicorn
from datetime import datetime

app = FastAPI(
    title="Advanced Data Generator API",
    description="REST API for generating realistic test data",
    version="1.0.0"
)

class GenerationRequest(BaseModel):
    num_users: Optional[int] = 10
    num_products: Optional[int] = 20
    num_orders: Optional[int] = 50
    locale: Optional[str] = "en_US"

class ExportRequest(BaseModel):
    format: str
    filters: Optional[Dict] = None

@app.post("/generate")
async def generate_data(request: GenerationRequest):
    try:
        generator = DataGenerator(locale=request.locale)
        generator.generate_data(
            request.num_users,
            request.num_products,
            request.num_orders
        )
        return {"message": "Data generated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/export")
async def export_data(request: ExportRequest):
    try:
        generator = DataGenerator()
        generator.export_data(request.format)
        return {"message": f"Data exported to {request.format} successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users")
async def get_users(limit: int = 100, offset: int = 0):
    try:
        generator = DataGenerator()
        users = generator.session.query(generator.User).offset(offset).limit(limit).all()
        return [user.__dict__ for user in users]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/products")
async def get_products(limit: int = 100, offset: int = 0):
    try:
        generator = DataGenerator()
        products = generator.session.query(generator.Product).offset(offset).limit(limit).all()
        return [product.__dict__ for product in products]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/orders")
async def get_orders(limit: int = 100, offset: int = 0):
    try:
        generator = DataGenerator()
        orders = generator.session.query(generator.Order).offset(offset).limit(limit).all()
        return [order.__dict__ for order in orders]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True) 