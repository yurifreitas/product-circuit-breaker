from pydantic import BaseModel, EmailStr, Field
from typing import List
from uuid import UUID
class User(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class MessageOut(BaseModel):
    message: str
    client_id: str

class ClientCreate(BaseModel):
    name: str = Field(..., example="João Silva")
    email: EmailStr = Field(..., example="joao@email.com")

class ClientOut(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    wishlist: List[str] = []

    class Config:
        orm_mode = True
        from_attributes = True
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "name": "João Silva",
                "email": "joao@email.com",
                "wishlist": ["1", "2", "3"]
            }
        }


class WishlistUpdate(BaseModel):
    product_id: str = Field(..., example="abc123")

class ProductOut(BaseModel):
    id: str = Field(..., example="abc123")
    title: str = Field(..., example="Smartphone Samsung Galaxy S20")
    image: str = Field(..., example="https://example.com/image.jpg")
    price: float = Field(..., example=1999.99)
    reviewScore: float | None = Field(None, example=4.5)

class WishlistOut(BaseModel):
    client_id: str = Field(..., example="3fa85f64-5717-4562-b3fc-2c963f66afa6")
    wishlist: List[ProductOut]

    class Config:
        json_schema_extra = {
            "example": {
                "client_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "wishlist": [
                    {
                        "id": "abc123",
                        "title": "Smartphone Samsung Galaxy S20",
                        "image": "https://example.com/image.jpg",
                        "price": 1999.99,
                        "reviewScore": 4.5
                    },
                    {
                        "id": "def456",
                        "title": "Smart TV LG 50” 4K",
                        "image": "https://example.com/tv.jpg",
                        "price": 2899.99,
                        "reviewScore": 4.7
                    }
                ]
            }
        }
