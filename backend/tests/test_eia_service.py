import pytest
from unittest.mock import Mock, patch
from services.eia_service import EIAClient

@pytest.fixture
def eia_client():
    return EIAClient(api_key="test_api_key")

def test_eia_client_initialization(eia_client):
    assert eia_client.api_key == "test_api_key"
    assert eia_client.BASE_URL == "https://api.eia.gov/v2"

@patch("services.eia_service.requests.Session.get")
def test_get_generation_data_success(mock_get, eia_client):
    mock_response = Mock()
    mock_response.json.return_value = {"data": []}
    mock_get.return_value = mock_response

    result = eia_client.get_generation_data("2024-01-01")
    assert result == {"data": []}
    mock_get.assert_called_once()

@patch("services.eia_service.requests.Session.get")
def test_get_generation_data_error(mock_get, eia_client):
    import requests
    mock_get.side_effect = requests.exceptions.ConnectionError("Connection failed")

    with pytest.raises(requests.exceptions.RequestException):
        eia_client.get_generation_data("2024-01-01")
