import os
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.models import Client

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

async def init_db():
    client = AsyncIOMotorClient(MONGO_URI)
    await init_beanie(database=client["wishlist_db"], document_models=[Client])
