from datetime import datetime, date
from database.db import SessionLocal, Base, engine
from models.generation import GenerationData
from models.pricing import PricingData
from models.renewable import RenewableData

# 테이블 생성
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# 더미 데이터
regions = ["CAISO", "ERCOT", "PJM", "MISO", "SPP", "WECC"]
today = date.today()

# 발전용량 데이터
for region in regions:
    gen = GenerationData(
        date=today,
        region=region,
        solar_capacity_mw=1500 + regions.index(region) * 200,
        wind_capacity_mw=3000 + regions.index(region) * 300,
        hydro_capacity_mw=800 + regions.index(region) * 100,
        fossil_capacity_mw=5000 + regions.index(region) * 500,
        nuclear_capacity_mw=2000 + regions.index(region) * 200,
        total_capacity_mw=12300 + regions.index(region) * 1300
    )
    db.add(gen)

# 가격 데이터
for region in regions:
    price = PricingData(
        date=today,
        region=region,
        price_per_mwh=45.50 + regions.index(region) * 5.25
    )
    db.add(price)

# 재생에너지 데이터
for region in regions:
    renewable = RenewableData(
        date=today,
        region=region,
        renewable_percentage=35.5 + regions.index(region) * 4.2,
        renewable_capacity_mw=2300 + regions.index(region) * 300,
        total_capacity_mw=12300 + regions.index(region) * 1300
    )
    db.add(renewable)

db.commit()
print("✅ Seed data inserted successfully!")
print(f"   - {len(regions)} regions")
print(f"   - Generation data: {len(regions)} records")
print(f"   - Pricing data: {len(regions)} records")
print(f"   - Renewable data: {len(regions)} records")
