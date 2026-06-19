import pytest
from datetime import datetime
from services.data_processor import DataProcessor
from models.generation import GenerationData
from models.pricing import PricingData
from models.renewable import RenewableData

class TestDataProcessor:
    def test_parse_generation_data_success(self):
        """발전 데이터 파싱 성공"""
        mock_response = {
            "data": [
                {
                    "respondent": "CAISO",
                    "type": "Solar",
                    "value": 1000.5,
                    "period": "2024-01-01"
                },
                {
                    "respondent": "CAISO",
                    "type": "Wind",
                    "value": 2000.3,
                    "period": "2024-01-01"
                }
            ]
        }

        records = DataProcessor.parse_generation_data(mock_response, "2024-01-01")

        assert len(records) == 2
        assert records[0].region == "CAISO"
        assert records[0].solar_capacity_mw == 1000.5
        assert records[1].wind_capacity_mw == 2000.3

    def test_parse_generation_data_empty(self):
        """발전 데이터 없음"""
        mock_response = {"data": []}
        records = DataProcessor.parse_generation_data(mock_response, "2024-01-01")
        assert len(records) == 0

    def test_parse_pricing_data_success(self):
        """가격 데이터 파싱 성공"""
        mock_response = {
            "data": [
                {
                    "respondent": "CAISO",
                    "value": 50.25,
                    "period": "2024-01-01"
                },
                {
                    "respondent": "ERCOT",
                    "value": 60.75,
                    "period": "2024-01-01"
                }
            ]
        }

        records = DataProcessor.parse_pricing_data(mock_response, "2024-01-01")

        assert len(records) == 2
        assert records[0].price_per_mwh == 50.25
        assert records[1].price_per_mwh == 60.75

    def test_parse_renewable_data_success(self):
        """재생에너지 데이터 파싱 성공"""
        mock_response = {
            "data": [
                {
                    "respondent": "CAISO",
                    "type": "Solar",
                    "value": 1500.0,
                    "total_capacity": 5000.0,
                    "period": "2024-01-01"
                }
            ]
        }

        records = DataProcessor.parse_renewable_data(mock_response, "2024-01-01")

        assert len(records) == 1
        assert records[0].renewable_capacity_mw == 1500.0
        assert records[0].renewable_percentage == 30.0

    def test_parse_data_with_invalid_values(self):
        """유효하지 않은 값 처리"""
        mock_response = {
            "data": [
                {
                    "respondent": "CAISO",
                    "type": "Solar",
                    "value": "invalid",
                    "period": "2024-01-01"
                }
            ]
        }

        records = DataProcessor.parse_generation_data(mock_response, "2024-01-01")
        # 유효하지 않은 데이터는 필터링됨
        assert len(records) == 0
