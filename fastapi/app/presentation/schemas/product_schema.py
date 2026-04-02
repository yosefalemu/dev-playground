from pydantic import BaseModel

class ProductCreateRequest(BaseModel):
    name: str
    stock: int
    price: float

class ProductPurchaseRequest(BaseModel):
    quantity: int

class ProductIncreaseStockRequest(BaseModel):
    quantity: int

class ProductSearchQuery(BaseModel):
    name: str | None = None
    min_price: float | None = None
    max_price: float | None = None