from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.application.services.product_service import ProductService
from app.domain.exceptions.product_exc import ProductNotFoundException
from app.infrastructure.repositories.product_repository_impl import ProductRepositoryImpl
from app.domain.entities.product import Product
from app.presentation.schemas.product_schema import ProductCreateRequest, ProductPurchaseRequest, ProductIncreaseStockRequest

router = APIRouter(
    prefix="/products",
    tags=["products"],
)

def product_service():
    product_respository = ProductRepositoryImpl()
    return ProductService(product_repository=product_respository)

@router.get("/")
async def get_products(product_service: ProductService = Depends(product_service)):
    return await product_service.get_products()

@router.get("/{product_id}")
async def get_product(product_id: int, product_service: ProductService = Depends(product_service)):
    return await product_service.get_product_by_id(product_id=product_id)

@router.get("/name/{product_name}")
async def get_product_by_name(product_name: str, product_service: ProductService = Depends(product_service)):
    return await product_service.get_product_by_name(name=product_name)

@router.post("/")
async def create_product(request: ProductCreateRequest, product_service: ProductService = Depends(product_service)):
    product = Product(
        id=None,
        name=request.name,
        stock=request.stock,
        price=request.price
    )
    return await product_service.create_product(product=product)

@router.delete("/{product_id}")
async def delete_product(product_id: int, product_service: ProductService = Depends(product_service)):
    return await product_service.delete_product(product_id=product_id)

@router.post("/{product_id}/purchase")
async def purchase_product(product_id: int, request: ProductPurchaseRequest, product_service: ProductService = Depends(product_service)):
    return await product_service.purchase_product(
        product_id=product_id,
        quantity=request.quantity
    )

@router.post("/{product_id}/increase_stock")
async def increase_stock(product_id: int, request:ProductIncreaseStockRequest, product_service: ProductService = Depends(product_service)):
    return await product_service.increase_stock(
        product_id=product_id,
        quantity=request.quantity
    )


