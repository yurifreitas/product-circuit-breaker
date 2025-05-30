import pytest
from httpx import AsyncClient
from uuid import uuid4

BASE_URL = "http://api:8001"


@pytest.mark.asyncio
async def get_access_token():
    payload = {"username": "testuser", "password": "mysecretpassword"}

    async with AsyncClient(base_url=BASE_URL) as ac:
        response = await ac.post("/auth/token", json=payload)
        assert response.status_code == 200
        return response.json()["access_token"]

@pytest.mark.asyncio
async def test_list_all_products():
    access_token = await get_access_token()
    HEADERS = {"Authorization": f"Bearer {access_token}"}

    async with AsyncClient(base_url=BASE_URL, headers=HEADERS) as ac:
        response = await ac.get("/product/products")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
