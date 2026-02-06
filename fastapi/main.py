from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    is_offer: bool = False

@app.get("/")
def read_root():
    return {"message" : "Hello FastAPI!"}

@app.get("/items")
def read_items():
    return {"message" : "Items"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}

@app.post("/items")
def create_item(item: Item):
    return {"item": item.name, "description": item.description, "price": item.price, "is_offer": item.is_offer}
//test