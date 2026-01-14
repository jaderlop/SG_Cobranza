from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.services.dashboard_service import *
from app.schemas.dashboard import *

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/kpis", response_model=KPIResponse)
def dashboard_kpis(db: Session = Depends(get_db)):
    return get_kpis(db)


@router.get("/sales-by-day", response_model=List[DailyAmount])
def dashboard_sales(db: Session = Depends(get_db)):
    return sales_by_day(db)


@router.get("/purchases-by-day", response_model=List[DailyAmount])
def dashboard_purchases(db: Session = Depends(get_db)):
    return purchases_by_day(db)


@router.get("/top-products", response_model=List[ProductRanking])
def dashboard_products(db: Session = Depends(get_db)):
    return top_products(db)
