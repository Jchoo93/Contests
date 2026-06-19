from sqlalchemy import Column, Integer, String, Float, Date, DateTime
from database.db import Base
from datetime import datetime

class PricingData(Base):
    __tablename__ = "pricing_data"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    region = Column(String, nullable=False, index=True)
    price_per_mwh = Column(Float, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    class Config:
        from_attributes = True
