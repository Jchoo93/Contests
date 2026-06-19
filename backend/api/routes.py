from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List

from database.db import get_db
from models.generation import GenerationData
from models.pricing import PricingData
from models.renewable import RenewableData
from api.schemas import GenerationDataResponse, PricingDataResponse, RenewableDataResponse, SummaryResponse

router = APIRouter(prefix="/api", tags=["power-grid"])

@router.get("/generation", response_model=List[GenerationDataResponse])
def get_generation_data(
    days: int = 1,
    db: Session = Depends(get_db)
):
    """지난 N일간의 발전 용량 데이터 조회"""
    cutoff_date = datetime.now().date() - timedelta(days=days)
    records = db.query(GenerationData).filter(
        GenerationData.date >= cutoff_date
    ).order_by(GenerationData.date.desc()).all()

    if not records:
        raise HTTPException(status_code=404, detail="No generation data found")

    return records

@router.get("/generation/{date}", response_model=List[GenerationDataResponse])
def get_generation_by_date(date: str, db: Session = Depends(get_db)):
    """특정 날짜의 발전 용량 데이터 조회"""
    try:
        query_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    records = db.query(GenerationData).filter(
        GenerationData.date == query_date
    ).all()

    if not records:
        raise HTTPException(status_code=404, detail="No generation data found for this date")

    return records

@router.get("/pricing", response_model=List[PricingDataResponse])
def get_pricing_data(
    days: int = 1,
    db: Session = Depends(get_db)
):
    """지난 N일간의 전력 가격 데이터 조회"""
    cutoff_date = datetime.now().date() - timedelta(days=days)
    records = db.query(PricingData).filter(
        PricingData.date >= cutoff_date
    ).order_by(PricingData.date.desc()).all()

    if not records:
        raise HTTPException(status_code=404, detail="No pricing data found")

    return records

@router.get("/pricing/{date}", response_model=List[PricingDataResponse])
def get_pricing_by_date(date: str, db: Session = Depends(get_db)):
    """특정 날짜의 전력 가격 데이터 조회"""
    try:
        query_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    records = db.query(PricingData).filter(
        PricingData.date == query_date
    ).all()

    if not records:
        raise HTTPException(status_code=404, detail="No pricing data found for this date")

    return records

@router.get("/renewables", response_model=List[RenewableDataResponse])
def get_renewable_data(
    days: int = 1,
    db: Session = Depends(get_db)
):
    """지난 N일간의 재생에너지 데이터 조회"""
    cutoff_date = datetime.now().date() - timedelta(days=days)
    records = db.query(RenewableData).filter(
        RenewableData.date >= cutoff_date
    ).order_by(RenewableData.date.desc()).all()

    if not records:
        raise HTTPException(status_code=404, detail="No renewable data found")

    return records

@router.get("/renewables/{date}", response_model=List[RenewableDataResponse])
def get_renewable_by_date(date: str, db: Session = Depends(get_db)):
    """특정 날짜의 재생에너지 데이터 조회"""
    try:
        query_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    records = db.query(RenewableData).filter(
        RenewableData.date == query_date
    ).all()

    if not records:
        raise HTTPException(status_code=404, detail="No renewable data found for this date")

    return records

@router.get("/summary", response_model=SummaryResponse)
def get_summary(db: Session = Depends(get_db)):
    """전력망 통합 요약"""
    today = datetime.now().date()

    gen_records = db.query(GenerationData).filter(GenerationData.date == today).all()
    pricing_records = db.query(PricingData).filter(PricingData.date == today).all()
    renewable_records = db.query(RenewableData).filter(RenewableData.date == today).all()

    if not gen_records or not pricing_records or not renewable_records:
        raise HTTPException(status_code=404, detail="Incomplete data for today")

    total_capacity = sum(
        (r.total_capacity_mw or 0) for r in gen_records
    ) / len(gen_records) if gen_records else 0

    renewable_pct = sum(
        r.renewable_percentage for r in renewable_records
    ) / len(renewable_records) if renewable_records else 0

    avg_price = sum(
        r.price_per_mwh for r in pricing_records
    ) / len(pricing_records) if pricing_records else 0

    return SummaryResponse(
        total_capacity_mw=total_capacity,
        renewable_percentage=renewable_pct,
        average_price_per_mwh=avg_price,
        regions_count=len(set(r.region for r in gen_records)),
        last_update=datetime.now()
    )

@router.get("/health")
def health_check():
    """헬스 체크"""
    return {"status": "ok", "timestamp": datetime.now().isoformat()}
