from pydantic import BaseModel

class ProductCreateRequest(BaseModel):
    name: str
    stock: int
    price: float

class ProductPurchaseRequest(BaseModel):
    quantity: int

class ProductIncreaseStockRequest(BaseModel):
    quantity: int