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
async def test_add_to_wishlist():
    client_id = str(uuid4())
    body = {
        "product_id": "tv456"
    }

    access_token = await get_access_token()
    HEADERS = {"Authorization": f"Bearer {access_token}"}

    async with AsyncClient(base_url=BASE_URL, headers=HEADERS) as ac:
        response = await ac.post(f"/wishlist/{client_id}/add", json=body)

    assert response.status_code == 404
    assert "client_id" in response.json()
    assert "wishlist" in response.json()


@pytest.mark.asyncio
async def test_remove_from_wishlist():
    client_id = str(uuid4())
    body = {
        "product_id": "abc123"
    }

    access_token = await get_access_token()
    HEADERS = {"Authorization": f"Bearer {access_token}"}

    async with AsyncClient(base_url=BASE_URL, headers=HEADERS) as ac:
        response = await ac.post(f"/wishlist/{client_id}/remove", json=body)

    assert response.status_code == 404
    assert "client_id" in response.json()
    assert "wishlist" in response.json()

