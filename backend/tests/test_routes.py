import pytest
from fastapi.testclient import TestClient
from datetime import datetime, date
from unittest.mock import patch, MagicMock
from app import app
from database.db import SessionLocal, Base, engine

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    """테스트용 데이터베이스 설정"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

class TestHealthEndpoint:
    def test_health_check(self):
        """헬스 체크 엔드포인트"""
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "timestamp" in data

class TestGenerationEndpoint:
    def test_generation_not_found(self):
        """생성 데이터 없음"""
        response = client.get("/api/generation?days=1")
        assert response.status_code == 404

    def test_generation_invalid_date_format(self):
        """잘못된 날짜 형식"""
        response = client.get("/api/generation/2024-13-45")
        assert response.status_code == 400

class TestPricingEndpoint:
    def test_pricing_not_found(self):
        """가격 데이터 없음"""
        response = client.get("/api/pricing?days=1")
        assert response.status_code == 404

    def test_pricing_invalid_date_format(self):
        """잘못된 날짜 형식"""
        response = client.get("/api/pricing/invalid-date")
        assert response.status_code == 400

class TestRenewableEndpoint:
    def test_renewable_not_found(self):
        """재생에너지 데이터 없음"""
        response = client.get("/api/renewables?days=1")
        assert response.status_code == 404

    def test_renewable_by_date_invalid_format(self):
        """잘못된 날짜 형식"""
        response = client.get("/api/renewables/2024/01/01")
        assert response.status_code == 404

class TestSummaryEndpoint:
    def test_summary_no_data(self):
        """요약 데이터 없음"""
        response = client.get("/api/summary")
        assert response.status_code == 404

class TestRootEndpoint:
    def test_root(self):
        """루트 엔드포인트"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "docs" in data
