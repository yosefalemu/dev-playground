from pydantic import BaseModel

class Item(BaseModel):
    id: int | None = None
    name: str
    description: str | None = None
    price: float
    tax: float | None = None