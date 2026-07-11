# app/features/products/product_models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.config.database import Base
from pydantic import BaseModel

class ProductDB(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    price = Column(Float)
    stock = Column(Integer)
    
    # Point directly to the table in the other domain
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("CategoryDB", back_populates="products")

class ProductCreate(BaseModel):
    title: str
    price: float
    stock: int
    category_name: str

class ProductResponse(BaseModel):
    id: int
    title: str
    price: float
    stock: int
    category_id: int

    class Config:
        from_attributes = True