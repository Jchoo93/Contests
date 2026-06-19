import logging
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional
from sqlalchemy.orm import Session

from models.generation import GenerationData
from models.pricing import PricingData
from models.renewable import RenewableData

logger = logging.getLogger(__name__)

class DataProcessor:
    """EIA API 데이터 처리"""

    @staticmethod
    def parse_generation_data(api_response: Dict, date: str) -> List[GenerationData]:
        """
        EIA API 발전 데이터 파싱 및 정규화
        Args:
            api_response: EIA API 응답
            date: YYYY-MM-DD 형식의 날짜
        Returns:
            GenerationData 객체 리스트
        """
        generation_records = []

        try:
            if "data" not in api_response:
                logger.warning(f"No data in API response for {date}")
                return generation_records

            data_list = api_response["data"]

            for row in data_list:
                try:
                    region = row.get("respondent", "Unknown")
                    gen_type = row.get("type", "").lower()
                    value = row.get("value")

                    if not value:
                        continue

                    record = GenerationData(
                        date=datetime.strptime(date, "%Y-%m-%d").date(),
                        region=region,
                    )

                    if "solar" in gen_type:
                        record.solar_capacity_mw = float(value)
                    elif "wind" in gen_type:
                        record.wind_capacity_mw = float(value)
                    elif "hydro" in gen_type:
                        record.hydro_capacity_mw = float(value)
                    elif "fossil" in gen_type or "coal" in gen_type or "natural gas" in gen_type:
                        record.fossil_capacity_mw = float(value)
                    elif "nuclear" in gen_type:
                        record.nuclear_capacity_mw = float(value)

                    generation_records.append(record)
                except (ValueError, TypeError) as e:
                    logger.warning(f"Error parsing generation record: {e}")
                    continue

        except Exception as e:
            logger.error(f"Error processing generation data: {e}")

        return generation_records

    @staticmethod
    def parse_pricing_data(api_response: Dict, date: str) -> List[PricingData]:
        """
        EIA API 가격 데이터 파싱 및 정규화
        Args:
            api_response: EIA API 응답
            date: YYYY-MM-DD 형식의 날짜
        Returns:
            PricingData 객체 리스트
        """
        pricing_records = []

        try:
            if "data" not in api_response:
                logger.warning(f"No data in API response for {date}")
                return pricing_records

            data_list = api_response["data"]

            for row in data_list:
                try:
                    region = row.get("respondent", "Unknown")
                    value = row.get("value")

                    if not value or not region:
                        continue

                    record = PricingData(
                        date=datetime.strptime(date, "%Y-%m-%d").date(),
                        region=region,
                        price_per_mwh=float(value)
                    )
                    pricing_records.append(record)
                except (ValueError, TypeError) as e:
                    logger.warning(f"Error parsing pricing record: {e}")
                    continue

        except Exception as e:
            logger.error(f"Error processing pricing data: {e}")

        return pricing_records

    @staticmethod
    def parse_renewable_data(api_response: Dict, date: str) -> List[RenewableData]:
        """
        EIA API 재생에너지 데이터 파싱 및 정규화
        Args:
            api_response: EIA API 응답
            date: YYYY-MM-DD 형식의 날짜
        Returns:
            RenewableData 객체 리스트
        """
        renewable_records = []

        try:
            if "data" not in api_response:
                logger.warning(f"No data in API response for {date}")
                return renewable_records

            data_list = api_response["data"]

            for row in data_list:
                try:
                    region = row.get("respondent", "Unknown")
                    gen_type = row.get("type", "").lower()
                    value = row.get("value")
                    total_capacity = row.get("total_capacity")

                    if not value or not region:
                        continue

                    renewable_percentage = 0.0
                    if total_capacity and total_capacity > 0:
                        renewable_percentage = (float(value) / float(total_capacity)) * 100

                    record = RenewableData(
                        date=datetime.strptime(date, "%Y-%m-%d").date(),
                        region=region,
                        renewable_percentage=renewable_percentage,
                        renewable_capacity_mw=float(value),
                        total_capacity_mw=float(total_capacity) if total_capacity else None
                    )
                    renewable_records.append(record)
                except (ValueError, TypeError) as e:
                    logger.warning(f"Error parsing renewable record: {e}")
                    continue

        except Exception as e:
            logger.error(f"Error processing renewable data: {e}")

        return renewable_records

    @staticmethod
    def aggregate_generation_data(db: Session, date: str) -> Dict:
        """
        일일 발전 데이터 집계
        Args:
            db: 데이터베이스 세션
            date: YYYY-MM-DD 형식의 날짜
        Returns:
            집계된 데이터
        """
        from datetime import datetime as dt
        query_date = dt.strptime(date, "%Y-%m-%d").date()

        records = db.query(GenerationData).filter(GenerationData.date == query_date).all()

        if not records:
            return {}

        df = pd.DataFrame([{
            'region': r.region,
            'solar': r.solar_capacity_mw or 0,
            'wind': r.wind_capacity_mw or 0,
            'hydro': r.hydro_capacity_mw or 0,
            'fossil': r.fossil_capacity_mw or 0,
            'nuclear': r.nuclear_capacity_mw or 0,
        } for r in records])

        grouped = df.groupby('region').sum().to_dict()
        return grouped
