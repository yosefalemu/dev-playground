from app.domain.repositories.product_repository import ProductRepository
from typing import Optional
from app.domain.entities.product import Product

class ProductService:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository
    async def get_product_by_id(self, product_id: int):
        return await self.product_repository.get_product_by_id(product_id=product_id)
    async def create_product(self, product):
        await self.product_repository.save_product(product=product)
    async def purchase_product(self, product_id: int, quantity: int):
        product: Optional[Product] = await self.product_repository.get_product_by_id(product_id=product_id)
        if not product:
            raise ValueError("Product not found")
        product.reduce_stock(quantity=quantity)
        await self.product_repository.save_product(product=product)
        return product
