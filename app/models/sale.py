from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base

class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("users.id"))
    total_amount = Column(Float)
    payment_method = Column(String)  # cash, card, mobile_money
    items = Column(JSON)  # Liste des produits vendus avec quantités et prix
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations
    employee = relationship("User")
