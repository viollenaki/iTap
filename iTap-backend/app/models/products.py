from pydantic import BaseModel

 
class Product(BaseModel): 
    name: str
    color: str
    weight: float
    height: float
    quantity: int
    price: float
     
class ProductIn(Product): 
    pass

class ProductOut(Product): 
    id: int