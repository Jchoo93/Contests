from sqlalchemy import Column, Integer, String, Float, Date, DateTime
from database.db import Base
from datetime import datetime

class GenerationMixTrend(Base):
    """발전원별 MIX 트렌드 추적"""
    __tablename__ = "generation_mix_trend"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    region = Column(String, nullable=False, index=True)

    # === 현재 발전원 구성 (%) ===
    solar_pct = Column(Float, nullable=False)
    wind_pct = Column(Float, nullable=False)
    hydro_pct = Column(Float, nullable=False)
    fossil_pct = Column(Float, nullable=False)
    nuclear_pct = Column(Float, nullable=False)
    renewable_total_pct = Column(Float, nullable=False)

    # === 7일 전 대비 변화 ===
    solar_pct_change_7d = Column(Float)
    wind_pct_change_7d = Column(Float)
    hydro_pct_change_7d = Column(Float)
    fossil_pct_change_7d = Column(Float)
    nuclear_pct_change_7d = Column(Float)
    renewable_pct_change_7d = Column(Float)

    # === 30일 전 대비 변화 ===
    solar_pct_change_30d = Column(Float)
    wind_pct_change_30d = Column(Float)
    renewable_pct_change_30d = Column(Float)

    # === 연간 변화 ===
    solar_pct_change_1y = Column(Float)
    wind_pct_change_1y = Column(Float)
    fossil_pct_change_1y = Column(Float)
    nuclear_pct_change_1y = Column(Float)
    renewable_pct_change_1y = Column(Float)

    # === 트렌드 방향 ===
    solar_trend = Column(String)      # "↑" / "→" / "↓"
    wind_trend = Column(String)
    hydro_trend = Column(String)
    fossil_trend = Column(String)
    nuclear_trend = Column(String)
    renewable_trend = Column(String)

    # === 변동성 (표준편차) ===
    solar_volatility = Column(Float)
    wind_volatility = Column(Float)
    hydro_volatility = Column(Float)
    renewable_volatility = Column(Float)

    # === 시장 지표 ===
    herfindahl_index = Column(Float)    # 시장 집중도 (다양성)
    energy_diversity_score = Column(Float)  # 0-10

    # === 타임스탬프 ===
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    class Config:
        from_attributes = True
