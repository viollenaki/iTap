from fastapi import Body, Depends, APIRouter

from app.models import products as product_models
from app.services import products as product_services


router = APIRouter(
    tags=["Products"],
    prefix="/products",
    responses={404: {"description": "Not found"}}
)

# Get all products
@router.get('/')
async def index(limit: int = 10, page: int = 1, search: str = ""):
    return await product_services.get_all_products(limit=limit, page=page, search=search)

# Get banque
@router.get("/{id}")
async def show(id: str):
    return await product_services.get_product(item_id=id)

# Store product
@router.post('/', status_code=201)
async def store(product: product_models.ProductIn = Body(...)):
    return await product_services.create_product(product=product.model_dump())

# Update product
@router.put('/{id}', status_code=200)
async def update(id: int, product: product_models.ProductIn = Body(...)):
    return await product_services.update_product(product_id=id, product_data=product.model_dump())

# Delete product
@router.delete('/{id}', status_code=200)
async def delete(id: int):
    return await product_services.delete_product(product_id=id)