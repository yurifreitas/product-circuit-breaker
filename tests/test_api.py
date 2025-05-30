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
async def test_create_client():
    email = f"{uuid4()}@test.com"
    payload = {"name": "Cliente Teste", "email": email}

    access_token = await get_access_token()

    HEADERS = {"Authorization": f"Bearer {access_token}"}

    async with AsyncClient(base_url=BASE_URL, headers=HEADERS) as ac:
        response = await ac.post("/clients/", json=payload)
        print("CREATE DEBUG:", response.status_code, response.text)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == payload["name"]
        assert data["email"] == payload["email"]
        assert "id" in data


@pytest.mark.asyncio
async def test_list_clients():
    access_token = await get_access_token()
    HEADERS = {"Authorization": f"Bearer {access_token}"}

    async with AsyncClient(base_url=BASE_URL, headers=HEADERS) as ac:
        response = await ac.get("/clients/")
        print("LIST DEBUG:", response.status_code, response.text)
        assert response.status_code == 200
        assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_client_by_id():
    email = f"{uuid4()}@test.com"
    payload = {"name": "Maria", "email": email}

    access_token = await get_access_token()
    HEADERS = {"Authorization": f"Bearer {access_token}"}

    async with AsyncClient(base_url=BASE_URL, headers=HEADERS) as ac:
        create = await ac.post("/clients/", json=payload)
        assert create.status_code == 200
        client_id = create.json()["id"]

        response = await ac.get(f"/clients/{client_id}")
        print("GET DEBUG:", response.status_code, response.text)
        assert response.status_code == 200
        assert response.json()["id"] == client_id
        assert response.json()["email"] == email


@pytest.mark.asyncio
async def test_delete_client():
    email = f"{uuid4()}@test.com"
    payload = {"name": "Carlos", "email": email}

    access_token = await get_access_token()
    HEADERS = {"Authorization": f"Bearer {access_token}"}

    async with AsyncClient(base_url=BASE_URL, headers=HEADERS) as ac:
        create = await ac.post("/clients/", json=payload)
        assert create.status_code == 200
        client_id = create.json()["id"]

        response = await ac.delete(f"/clients/{client_id}")
        print("DELETE DEBUG:", response.status_code, response.text)
        assert response.status_code == 200
        assert response.json()["message"] == "Cliente removido com sucesso"

        confirm = await ac.get(f"/clients/{client_id}")
        assert confirm.status_code == 404


@pytest.mark.asyncio
async def test_create_client_duplicate_email():
    email = f"{uuid4()}@test.com"
    payload = {"name": "Duplicado", "email": email}

    access_token = await get_access_token()
    HEADERS = {"Authorization": f"Bearer {access_token}"}

    async with AsyncClient(base_url=BASE_URL, headers=HEADERS) as ac:
        res1 = await ac.post("/clients/", json=payload)
        assert res1.status_code == 200

        res2 = await ac.post("/clients/", json=payload)
        print("DUPLICATE DEBUG:", res2.status_code, res2.text)
        assert res2.status_code == 400
        assert res2.json()["detail"] == "Email já registrado."


@pytest.mark.asyncio
async def test_auth_required():
    async with AsyncClient(base_url=BASE_URL) as ac:
        response = await ac.get("/clients/")
        assert response.status_code == 403
        assert response.json()["detail"] == "Not authenticated"
