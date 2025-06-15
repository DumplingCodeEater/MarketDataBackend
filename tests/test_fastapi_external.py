import pytest
import requests

def test_fastapi_app_is_responsive():
    """
    Tests if the FastAPI application is responsive by hitting the /docs endpoint
    exposed by the running Docker container on localhost:8000.
    """
    response = requests.get("http://localhost:8000/docs")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "").lower()

def test_get_latest_price():
    response = requests.get("http://localhost:8000/prices/latest?symbol=MSFT&provider=finnhub")
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "MSFT"
    assert isinstance(data["price"], (float, int))
    assert data["provider"] == "finnhub"

def test_poll_prices():
    response = requests.post(
        "http://localhost:8000/prices/poll",
        json={"symbols": ["AAPL", "MSFT"], "interval": 60, "provider": "alpha_vantage"}
    )
    assert response.status_code == 202
    data = response.json()
    assert data["status"] == "accepted"
    assert "job_id" in data
    assert data["config"]["symbols"] == ["AAPL", "MSFT"]
    assert data["config"]["interval"] == 60
