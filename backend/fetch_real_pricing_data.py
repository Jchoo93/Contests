"""
실제 EIA API에서 전력 가격 데이터를 받아오는 스크립트
"""
import requests
import logging
from datetime import datetime, timedelta
from database.db import SessionLocal, Base, engine
from models.pricing import PricingData
from config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)
db = SessionLocal()

def fetch_real_pricing_data():
    """EIA API에서 실제 전력 가격 데이터 조회"""

    # 어제 데이터 조회
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    print(f"\n📊 EIA API에서 {yesterday} 전력 가격 데이터 조회 중...")
    print(f"API Key: {settings.eia_api_key}")

    try:
        endpoint = "https://api.eia.gov/v2/electricity/rto/region-data/data"
        params = {
            "api_key": settings.eia_api_key,
            "data[0]": "value",
            "facets[type][]": ["Average Price Received by Utilities"],
            "start": yesterday,
            "end": yesterday,
            "sort": [{"column": "period", "direction": "desc"}],
            "offset": 0,
            "length": 10000
        }

        response = requests.get(endpoint, params=params, timeout=30)
        response.raise_for_status()

        data = response.json()

        if "data" not in data:
            print("⚠️ API 응답에 데이터가 없습니다")
            print(f"응답: {data}")
            return

        records = data.get("data", [])

        if not records:
            print("⚠️ 조회 가능한 데이터가 없습니다")
            return

        print(f"\n✅ {len(records)}개의 레코드를 받았습니다\n")

        # 지역별 가격 정보
        regions_data = {}
        for record in records:
            region = record.get("respondent", "Unknown")
            value = record.get("value")

            if value and region not in regions_data:
                regions_data[region] = {
                    "price": float(value),
                    "type": record.get("type", ""),
                    "period": record.get("period", "")
                }

        # 출력
        print("=" * 70)
        print(f"📍 미국 전력 지역별 가격 ({yesterday})")
        print("=" * 70)

        for region, data in sorted(regions_data.items()):
            price = data['price']
            print(f"\n🔌 {region}")
            print(f"   가격:      ${price:.2f}/MWh")
            print(f"   타입:      {data['type']}")
            print(f"   기간:      {data['period']}")

        print("\n" + "=" * 70)

        # 데이터베이스에 저장
        print("\n💾 데이터베이스에 저장 중...")

        for region, data in regions_data.items():
            # 기존 데이터 삭제
            db.query(PricingData).filter(
                PricingData.date == yesterday,
                PricingData.region == region
            ).delete()

            # 새 데이터 추가
            pricing = PricingData(
                date=datetime.strptime(yesterday, "%Y-%m-%d").date(),
                region=region,
                price_per_mwh=data['price']
            )
            db.add(pricing)

        db.commit()
        print(f"✅ {len(regions_data)}개 지역의 실제 가격 데이터 저장 완료!")

        return regions_data

    except requests.exceptions.RequestException as e:
        print(f"❌ API 요청 실패: {e}")
        return None
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return None
    finally:
        db.close()

if __name__ == "__main__":
    fetch_real_pricing_data()
