from datetime import datetime, date, timedelta
from database.db import SessionLocal, Base, engine
from models.generation import GenerationData
from models.mix_trend import GenerationMixTrend
from services.mix_trend_calculator import MixTrendCalculator

# 테이블 생성
Base.metadata.create_all(bind=engine)

db = SessionLocal()

regions = ["CAISO", "ERCOT", "PJM", "MISO", "SPP", "WECC"]
today = date.today()

print("🔄 발전원 MIX 트렌드 데이터 생성 중...")

# 지난 30일 데이터 생성 (트렌드 계산용)
for days_back in range(30, -1, -1):
    current_date = today - timedelta(days=days_back)

    for idx, region in enumerate(regions):
        # 각 지역마다 다른 기본값으로 생성
        base_solar = 1500 + idx * 200 + (30 - days_back) * 20  # 시간이 갈수록 증가
        base_wind = 3000 + idx * 300 - (30 - days_back) * 15   # 시간이 갈수록 감소
        base_hydro = 800 + idx * 100
        base_fossil = 5000 + idx * 500 - (30 - days_back) * 30  # 시간이 갈수록 감소
        base_nuclear = 2000 + idx * 200

        # GenerationData 생성
        gen = GenerationData(
            date=current_date,
            region=region,
            solar_capacity_mw=base_solar,
            wind_capacity_mw=base_wind,
            hydro_capacity_mw=base_hydro,
            fossil_capacity_mw=base_fossil,
            nuclear_capacity_mw=base_nuclear,
            total_capacity_mw=base_solar + base_wind + base_hydro + base_fossil + base_nuclear
        )
        db.add(gen)

db.commit()
print("✅ GenerationData 생성 완료 (30일)")

# GenerationMixTrend 데이터 생성
print("🔄 GenerationMixTrend 데이터 생성 중...")

for days_back in range(7, -1, -1):
    current_date = today - timedelta(days=days_back)

    # 해당 날짜의 GenerationData 조회
    gen_records = db.query(GenerationData).filter(
        GenerationData.date == current_date
    ).all()

    for gen in gen_records:
        # 트렌드 레코드 생성
        trend_record = MixTrendCalculator.create_mix_trend_record(
            db, gen.region, current_date, gen
        )
        db.add(trend_record)

db.commit()
print("✅ GenerationMixTrend 생성 완료")

# 최신 데이터 확인
latest_trends = db.query(GenerationMixTrend).filter(
    GenerationMixTrend.date == today
).all()

print("\n" + "="*70)
print(f"📊 최신 발전원 MIX 트렌드 (오늘: {today})")
print("="*70)

for trend in sorted(latest_trends, key=lambda x: x.renewable_total_pct, reverse=True):
    print(f"\n🔌 {trend.region}")
    print(f"   태양광:      {trend.solar_pct:5.1f}% {trend.solar_trend} ({trend.solar_pct_change_7d:+.1f}% 7d)")
    print(f"   풍력:        {trend.wind_pct:5.1f}% {trend.wind_trend} ({trend.wind_pct_change_7d:+.1f}% 7d)")
    print(f"   수력:        {trend.hydro_pct:5.1f}% {trend.hydro_trend}")
    print(f"   화석:        {trend.fossil_pct:5.1f}% {trend.fossil_trend} ({trend.fossil_pct_change_7d:+.1f}% 7d)")
    print(f"   원자력:      {trend.nuclear_pct:5.1f}% {trend.nuclear_trend}")
    print(f"   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"   재생에너지:   {trend.renewable_total_pct:5.1f}% {trend.renewable_trend} ({trend.renewable_pct_change_7d:+.1f}% 7d)")
    print(f"   다양성 점수: {trend.energy_diversity_score:.1f}/10")
    print(f"   변동성:      ☀️={trend.solar_volatility:.1f}% 💨={trend.wind_volatility:.1f}%")

print("\n" + "="*70)
print("✅ Seed data successfully created!")
print("="*70)
