from sqlalchemy import Column, Integer, String, Float, Date, DateTime, func
from database.db import Base
from datetime import datetime

class GenerationData(Base):
    __tablename__ = "generation_data"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    region = Column(String, nullable=False, index=True)

    solar_capacity_mw = Column(Float, nullable=True)
    wind_capacity_mw = Column(Float, nullable=True)
    hydro_capacity_mw = Column(Float, nullable=True)
    fossil_capacity_mw = Column(Float, nullable=True)
    nuclear_capacity_mw = Column(Float, nullable=True)
    total_capacity_mw = Column(Float, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    class Config:
        from_attributes = True
