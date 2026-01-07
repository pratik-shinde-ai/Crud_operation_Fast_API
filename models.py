#SQLAlchemy – DB Table)
from sqlalchemy import Column, Integer, String, Float
from database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)






















# from pydantic import BaseModel

# class Product(BaseModel):
#     id:int
#     name:str
#     description:str
#     price:float
#     quantity:int
