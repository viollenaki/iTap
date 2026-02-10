from sqlalchemy.orm import relationship 
from sqlalchemy.orm import declarative_base 
from sqlalchemy import Column, Integer, String, Double

Base = declarative_base() 

class Products(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True) 
    name = Column(String(225))
    color = Column(String(225))
    weight = Column(Double)
    height = Column(Double)
    quantity = Column(Integer)
    price = Column(Double)