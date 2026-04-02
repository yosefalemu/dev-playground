from fastapi import APIRouter, Depends, Query
from typing import Annotated

from app.application.services.product_service import ProductService
from app.infrastructure.repositories.product_repository_impl import ProductRepositoryImpl
from app.domain.entities.product import Product
from app.presentation.schemas.product_schema import ProductCreateRequest, ProductPurchaseRequest, ProductIncreaseStockRequest
from app.domain.filters.product_filters import ProductSearchFilters
from app.presentation.schemas.product_schema import ProductSearchQuery

router = APIRouter(
    prefix="/products",
    tags=["products"],
)

def product_service():
    product_respository = ProductRepositoryImpl()
    return ProductService(product_repository=product_respository)

ProductServiceType = Annotated[ProductService, Depends(product_service)]

@router.get("/")
async def get_products(product_service: ProductServiceType):
    return await product_service.get_products()

@router.get("/search")
async def search_products(
    product_service: ProductServiceType,
    request: Annotated[ProductSearchQuery, Query()]
    
):
    return await product_service.search_products(
        filters=ProductSearchFilters(
            name=request.name,
            min_price=request.min_price,
            max_price=request.max_price,
        )
    )

@router.get("/{product_id}")
async def get_product(product_id: int, product_service: ProductServiceType):
    return await product_service.get_product_by_id(product_id=product_id)

@router.get("/name/{product_name}")
async def get_product_by_name(product_name: str, product_service: ProductServiceType):
    return await product_service.get_product_by_name(name=product_name)

@router.post("/")
async def create_product(request: ProductCreateRequest, product_service: ProductServiceType):
    product = Product(
        id=None,
        name=request.name,
        stock=request.stock,
        price=request.price
    )
    return await product_service.create_product(product=product)

@router.delete("/{product_id}")
async def delete_product(product_id: int, product_service: ProductServiceType):
    return await product_service.delete_product(product_id=product_id)

@router.post("/{product_id}/purchase")
async def purchase_product(product_id: int, request: ProductPurchaseRequest, product_service: ProductServiceType):
    return await product_service.purchase_product(
        product_id=product_id,
        quantity=request.quantity
    )

@router.post("/{product_id}/increase_stock")
async def increase_stock(product_id: int, request:ProductIncreaseStockRequest, product_service: ProductServiceType):
    return await product_service.increase_stock(
        product_id=product_id,
        quantity=request.quantity
    )




