from fastapi import HTTPException

from app.configs.tables import Products
from app.utils import db_utils as db

async def get_all_products(limit: int = 10, page: int = 1, search: str = ""):
    try:
        products = await db.get_all(Products)
        # TODO: implement pagination and search
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching products: {e}") from e
    
async def get_product(item_id):
    try:
        product = await db.get_by_id(Products, item_id)
        return product
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching product: {e}") from e
    
async def create_product(payload):
    try:
        new_product = await db.create(Products, payload)
        return new_product
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating product: {e}") from e
    
async def update_product(product_id, payload):
    try:
        updated_product = await db.update(Products, product_id, payload)
        return updated_product
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating product: {e}") from e
    
async def delete_product(product_id):
    try:
        await db.delete(Products, product_id)
        return {"detail": "Permission deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting product: {e}") from e