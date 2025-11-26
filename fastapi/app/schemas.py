from pydantic import BaseModel, Field, validator

class ProductCreate(BaseModel):
    name: str
    price: float
    description: str | None = None
    
    @validator("name")
    def name_must_not_be_empty(cls, v):
        stripped = v.strip()
        if not stripped:
            raise ValueError("Name cannot be empty")
        if len(stripped) < 3:
            raise ValueError("Name must be at least 3 characters long")
        if len(stripped) > 50:
            raise ValueError("Name must be at most 50 characters long")
        return stripped
    @validator("price")
    def price_must_be_valid(cls, v):
        if v is None:
            raise ValueError("Price is required")
        if not isinstance(v, (float, int)):
            raise TypeError("Price must be a number(float)")
        if v <= 0:
            raise ValueError("Price must be greater than 0")
        if v >= 100:
            raise ValueError("Price must be less than 100")
        return float(v)

class ProductRead(ProductCreate):
    id: int
    
class GetSingleProductRequest(BaseModel):
    product_id: int
