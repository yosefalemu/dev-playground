from app.domain.repositories.product_repository import ProductRepository
from typing import Optional
from app.domain.entities.product import Product

class ProductService:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository
    async def get_products(self) -> list[Product]:
        return await self.product_repository.get_products()
    async def get_product_by_id(self, product_id: int) -> Optional[Product]:
        return await self.product_repository.get_product_by_id(product_id=product_id)
    async def get_product_by_name(self, name: str) -> Optional[Product]:
        return await self.product_repository.get_product_by_name(name=name)
    async def create_product(self, product: Product) -> Product:
        existing_product_by_name = await self.product_repository.get_product_by_name(name=product.name)
        if existing_product_by_name:
            raise ValueError(f"Product with name {product.name} already exists")
        return await self.product_repository.create_product(product=product)
    async def delete_product(self, product_id: int) -> Optional[Product]:
        deleted_product = await self.product_repository.delete_product(product_id=product_id)
        if not deleted_product:
            raise ValueError(f"Product with id {product_id} not found")
        return deleted_product
