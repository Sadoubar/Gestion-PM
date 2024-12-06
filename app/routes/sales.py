from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from ..database import get_db
from ..models.sale import Sale

router = APIRouter()

@router.get("/")
def get_sales(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    sales = db.query(Sale).offset(skip).limit(limit).all()
    return sales

@router.post("/")
def create_sale(sale: dict, db: Session = Depends(get_db)):
    db_sale = Sale(**sale)
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return db_sale

@router.get("/{sale_id}")
def get_sale(sale_id: int, db: Session = Depends(get_db)):
    sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if sale is None:
        raise HTTPException(status_code=404, detail="Vente non trouvée")
    return sale

@router.get("/daily-report")
def get_daily_report(date: datetime = None, db: Session = Depends(get_db)):
    if date is None:
        date = datetime.now()
    
    sales = db.query(Sale).filter(
        Sale.created_at >= date.replace(hour=0, minute=0, second=0),
        Sale.created_at <= date.replace(hour=23, minute=59, second=59)
    ).all()
    
    total_sales = sum(sale.total_amount for sale in sales)
    return {
        "date": date.date(),
        "total_sales": total_sales,
        "number_of_sales": len(sales),
        "sales": sales
    }

@router.get("/monthly-report")
def get_monthly_report(year: int, month: int, db: Session = Depends(get_db)):
    sales = db.query(Sale).filter(
        Sale.created_at >= datetime(year, month, 1),
        Sale.created_at < datetime(year, month + 1, 1) if month < 12 else datetime(year + 1, 1, 1)
    ).all()
    
    total_sales = sum(sale.total_amount for sale in sales)
    return {
        "year": year,
        "month": month,
        "total_sales": total_sales,
        "number_of_sales": len(sales),
        "sales": sales
    }
