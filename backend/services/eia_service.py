import requests
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, List
from config import settings

logger = logging.getLogger(__name__)

class EIAClient:
    """EIA API 클라이언트"""
    BASE_URL = "https://api.eia.gov/v2"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()

    def get_generation_data(self, date: str) -> Dict:
        """
        발전원별 발전량 데이터 조회
        Args:
            date: YYYY-MM-DD 형식의 날짜 문자열
        Returns:
            발전량 데이터 딕셔너리
        """
        try:
            endpoint = f"{self.BASE_URL}/electricity/rto/region-data/data"
            params = {
                "api_key": self.api_key,
                "data[0]": "value",
                "facets[respondent][]": ["US48"],
                "start": date,
                "end": date,
                "sort": [{"column": "period", "direction": "desc"}],
                "offset": 0,
                "length": 10000
            }
            response = self.session.get(endpoint, params=params, timeout=30)
            response.raise_for_status()
            logger.info(f"Successfully fetched generation data for {date}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching generation data: {e}")
            raise

    def get_pricing_data(self, date: str) -> Dict:
        """
        지역별 전력 가격 데이터 조회
        Args:
            date: YYYY-MM-DD 형식의 날짜 문자열
        Returns:
            가격 데이터 딕셔너리
        """
        try:
            endpoint = f"{self.BASE_URL}/electricity/rto/region-data/data"
            params = {
                "api_key": self.api_key,
                "data[0]": "value",
                "facets[type][]": ["Average Price Received by Utilities"],
                "start": date,
                "end": date,
                "sort": [{"column": "period", "direction": "desc"}],
                "offset": 0,
                "length": 10000
            }
            response = self.session.get(endpoint, params=params, timeout=30)
            response.raise_for_status()
            logger.info(f"Successfully fetched pricing data for {date}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching pricing data: {e}")
            raise

    def get_renewable_data(self, date: str) -> Dict:
        """
        재생에너지 데이터 조회
        Args:
            date: YYYY-MM-DD 형식의 날짜 문자열
        Returns:
            재생에너지 데이터 딕셔너리
        """
        try:
            endpoint = f"{self.BASE_URL}/electricity/rto/region-data/data"
            params = {
                "api_key": self.api_key,
                "data[0]": "value",
                "facets[type][]": ["Solar", "Wind", "Hydro"],
                "start": date,
                "end": date,
                "sort": [{"column": "period", "direction": "desc"}],
                "offset": 0,
                "length": 10000
            }
            response = self.session.get(endpoint, params=params, timeout=30)
            response.raise_for_status()
            logger.info(f"Successfully fetched renewable data for {date}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching renewable data: {e}")
            raise

    def close(self):
        """세션 종료"""
        self.session.close()
