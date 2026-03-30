from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.application.services.product_service import ProductService
from app.infrastructure.repositories.product_repository_impl import ProductRepositoryImpl
from app.domain.entities.product import Product

router = APIRouter(
    prefix="/products",
    tags=["products"],
)

class ProductCreateRequest(BaseModel):
    id: int
    name: str
    stock: int
    price: float

class ProductPurchaseRequest(BaseModel):
    quantity: int


def get_product_service():
    product_respository = ProductRepositoryImpl()
    return ProductService(product_repository=product_respository)

@router.post("/")
async def create_product(request: ProductCreateRequest, product_service: ProductService = Depends(get_product_service)):
    product = Product(
        id=request.id,
        name=request.name,
        stock=request.stock,
        price=request.price
    )
    return await product_service.create_product(product=product)

@router.get("/{product_id}")
async def get_product(product_id: int, product_service: ProductService = Depends(get_product_service)):
    return await product_service.get_product_by_id(product_id=product_id)

@router.post("/{product_id}/purchase")
async def purchase_product(product_id: int, request: ProductPurchaseRequest, product_service: ProductService = Depends(get_product_service)):
    return await product_service.purchase_product(
        product_id=product_id,
        quantity=request.quantity
    )

