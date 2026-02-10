from fastapi import Body, Depends, APIRouter
from fastapi.responses import JSONResponse

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
    products = await product_services.get_all_products(limit=limit, page=page, search=search)
    return JSONResponse(content={"products": products})

# Get banque
@router.get("/{id}")
async def show(id: str):
    product = await product_services.get_product(item_id=id)
    return JSONResponse(content={"product": product})

# Store product
@router.post('/', status_code=201)
async def store(product: product_models.ProductIn = Body(...)):
    new_product = await product_services.create_product(product=product.model_dump())
    return JSONResponse(content={"product": new_product})

# Update product
@router.put('/{id}', status_code=200)
async def update(id: int, product: product_models.ProductIn = Body(...)):
    updated_product = await product_services.update_product(product_id=id, product_data=product.model_dump())
    return JSONResponse(content={"product": updated_product})

# Delete product
@router.delete('/{id}', status_code=200)
async def delete(id: int):
    result = await product_services.delete_product(product_id=id)
    return JSONResponse(content={"result": result})