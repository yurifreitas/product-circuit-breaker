from beanie import Document
from pydantic import EmailStr, Field
from typing import List
from uuid import UUID, uuid4

class Client(Document):
    id: UUID = Field(default_factory=uuid4, alias="_id")
    name: str
    email: EmailStr
    wishlist: List[str] = []

    class Settings:
        name = "clients"
        indexes = [
            "email"
        ]

    class Config:
        from_attributes = True
        populate_by_name = True
