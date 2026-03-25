import uuid
from pydantic import BaseModel

class ItemBase(BaseModel):
    id: uuid.UUID
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

class ItemCreate(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

class ItemUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    tax: float | None = None