from sqlalchemy import Column, Integer, String, Float, Date, DateTime
from database.db import Base
from datetime import datetime

class RenewableData(Base):
    __tablename__ = "renewable_data"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    region = Column(String, nullable=False, index=True)
    renewable_percentage = Column(Float, nullable=False)
    renewable_capacity_mw = Column(Float, nullable=True)
    total_capacity_mw = Column(Float, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    class Config:
        from_attributes = True
