from fastapi import APIRouter, HTTPException
from app.models import Client
from app.schemas import ClientCreate, ClientOut, MessageOut
from uuid import UUID
router = APIRouter()

@router.post("/", response_model=ClientOut)
async def create_client(data: ClientCreate):
    if await Client.find_one(Client.email == data.email):
        raise HTTPException(status_code=400, detail="Email já registrado.")
    client = Client(name=data.name, email=data.email)
    await client.insert()
    return ClientOut.model_validate(client, from_attributes=True)

@router.get("/", response_model=list[ClientOut])
async def list_clients():
    return await Client.find_all().to_list()

@router.get("/{client_id}", response_model=ClientOut)
async def get_client(client_id: str):
    client = await Client.get(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return client

@router.delete("/{client_id}", response_model=MessageOut)
async def delete_client(client_id: UUID):
    client = await Client.get(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    await client.delete()
    return {"message": "Cliente removido com sucesso", "client_id": str(client.id)}


@router.put("/{client_id}", response_model=ClientOut)
async def update_client(client_id: UUID, data: ClientCreate):
    client = await Client.get(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    if data.email != client.email and await Client.find_one(Client.email == data.email):
        raise HTTPException(status_code=400, detail="Email já registrado.")
    client.name = data.name
    client.email = data.email
    await client.save()
    return ClientOut.model_validate(client, from_attributes=True)