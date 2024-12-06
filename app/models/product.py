from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from ..database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    barcode = Column(String, unique=True, index=True)
    price = Column(Float)
    cost_price = Column(Float)
    stock_quantity = Column(Integer, default=0)
    minimum_stock = Column(Integer, default=5)
    category = Column(String, index=True)
    supplier = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
