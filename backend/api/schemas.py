from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, List

class GenerationDataResponse(BaseModel):
    id: int
    date: date
    region: str
    solar_capacity_mw: Optional[float] = None
    wind_capacity_mw: Optional[float] = None
    hydro_capacity_mw: Optional[float] = None
    fossil_capacity_mw: Optional[float] = None
    nuclear_capacity_mw: Optional[float] = None
    total_capacity_mw: Optional[float] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PricingDataResponse(BaseModel):
    id: int
    date: date
    region: str
    price_per_mwh: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class RenewableDataResponse(BaseModel):
    id: int
    date: date
    region: str
    renewable_percentage: float
    renewable_capacity_mw: Optional[float] = None
    total_capacity_mw: Optional[float] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class SummaryResponse(BaseModel):
    total_capacity_mw: float
    renewable_percentage: float
    average_price_per_mwh: float
    regions_count: int
    last_update: datetime
