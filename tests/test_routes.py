import pytest

@pytest.mark.asyncio
async def test_get_latest_price(client):
    response = await client.get("/prices/latest?symbol=AAPL")
    assert response.status_code == 200
    data = response.json()
    assert "price" in data
    assert isinstance(data["price"], (float, int))


