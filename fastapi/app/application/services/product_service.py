from app.application.dto.product_dto import ProductListResponseDTO
from app.domain.exceptions.product_exc import ProductAlreadyExistsException, ProductNotFoundException, ProductOutofStockException, InsufficientStockException
from app.domain.repositories.product_repository import ProductRepository
from typing import Optional,cast
from app.domain.entities.product import Product

class ProductService:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository
    async def get_products(self) -> ProductListResponseDTO:
        products, count = await self.product_repository.get_products()
        return ProductListResponseDTO(products=products, count=count)
    async def get_product_by_id(self, product_id: int) -> Optional[Product]:
        product_found = await self.product_repository.get_product_by_id(product_id=product_id)
        if not product_found:
            raise ProductNotFoundException(f"Product with id {product_id} not found")
        return product_found
    async def get_product_by_name(self, name: str) -> Optional[Product]:
        product_found = await self.product_repository.get_product_by_name(name=name)
        if not product_found:
            raise ProductNotFoundException(f"Product with name {name} not found")
        return product_found
    async def create_product(self, product: Product) -> Product:
        existing_product_by_name = await self.product_repository.get_product_by_name(name=product.name)
        if existing_product_by_name:
            raise ProductAlreadyExistsException(f"Product with name {product.name} already exists")
        return await self.product_repository.create_product(product=product)
    async def delete_product(self, product_id: int) -> Optional[Product]:
        deleted_product = await self.product_repository.delete_product(product_id=product_id)
        if not deleted_product:
            raise ProductNotFoundException(f"Product with id {product_id} not found")
        return deleted_product
    async def purchase_product(self, product_id: int, quantity: int) -> Product:
        product_found = await self.product_repository.get_product_by_id(product_id=product_id)
        if not product_found:
            raise ProductNotFoundException(f"Product with id {product_id} not found")
        product_found = cast(Product, product_found)
        if product_found.stock == 0:
            raise ProductOutofStockException(f"Product with id {product_id} is out of stock")
        if product_found.stock < quantity:
            raise InsufficientStockException(f"Product with id {product_id} has insufficient stock")
        return await self.product_repository.purchase_product(product_id=product_id, quantity=quantity)
    
    async def increase_stock(self, product_id: int, quantity: int) -> Product:
        product_found = await self.product_repository.get_product_by_id(product_id=product_id)
        if not product_found:
            raise ProductNotFoundException(f"Product with id {product_id} not found")
        return await self.product_repository.increase_stock(product_id=product_id, quantity=quantity)

