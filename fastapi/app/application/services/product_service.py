from app.application.dto.product_dto import ProductListResponseDTO, ProductResponseDTO, ProductResponseForUserDTO
from app.domain.exceptions.product_exc import ProductAlreadyExistsException, ProductNotFoundException, ProductOutofStockException, InsufficientStockException
from app.domain.repositories.product_repository import ProductRepository
from typing import Optional,cast
from app.domain.entities.product import Product

class ProductService:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository
    
    async def get_products(self) -> ProductListResponseDTO:
        products, count = await self.product_repository.get_products()
        products = cast(list[Product], products)
        product_dtos = [
            ProductResponseForUserDTO(
                id=product.id,
                name=product.name,
                price=product.price
            )
            for product in products
        ]
        return ProductListResponseDTO(products=product_dtos, count=count)
    
    async def get_product_by_id(self, product_id: int) -> Optional[ProductResponseForUserDTO]:
        product_found = await self.product_repository.get_product_by_id(product_id=product_id)
        if not product_found:
            raise ProductNotFoundException(f"Product with id {product_id} not found")
        product_found = cast(Product, product_found)
        return ProductResponseForUserDTO(
            id=product_found.id,
            name=product_found.name,
            price=product_found.price
        )
    
    async def get_product_by_name(self, name: str) -> Optional[ProductResponseForUserDTO]:
        product_found = await self.product_repository.get_product_by_name(name=name)
        if not product_found:
            raise ProductNotFoundException(f"Product with name {name} not found")
        product_found = cast(Product, product_found)
        return ProductResponseForUserDTO(
            id=product_found.id,
            name=product_found.name,
            price=product_found.price
        )
    
    async def purchase_product(self, product_id: int, quantity: int) -> ProductResponseForUserDTO:
        product_found = await self.product_repository.get_product_by_id(product_id=product_id)
        if not product_found:
            raise ProductNotFoundException(f"Product with id {product_id} not found")
        product_found = cast(Product, product_found)
        if product_found.stock == 0:
            raise ProductOutofStockException(f"Product with id {product_id} is out of stock")
        if product_found.stock < quantity:
            raise InsufficientStockException(f"Product with id {product_id} has insufficient stock")
        purchased_product = await self.product_repository.purchase_product(product_id=product_id, quantity=quantity)
        if not purchased_product:
            raise ProductNotFoundException(f"Product with id {product_id} not found")
        return ProductResponseForUserDTO(
            id=purchased_product.id,
            name=purchased_product.name,
            price=purchased_product.price
        )
    

    # For the admin to create, delete and increase stock of products
    # I will implement authentication and authorization later, for now I will just implement the functionality without any authentication and authorization
    async def create_product(self, product: Product) -> ProductResponseDTO:
        existing_product_by_name = await self.product_repository.get_product_by_name(name=product.name)
        if existing_product_by_name:
            raise ProductAlreadyExistsException(f"Product with name {product.name} already exists")
        return await self.product_repository.create_product(product=product)
    
    async def delete_product(self, product_id: int) -> Optional[ProductResponseDTO]:
        deleted_product = await self.product_repository.delete_product(product_id=product_id)
        if not deleted_product:
            raise ProductNotFoundException(f"Product with id {product_id} not found")
        return deleted_product
    

    async def increase_stock(self, product_id: int, quantity: int) -> ProductResponseDTO:
        product_found = await self.product_repository.get_product_by_id(product_id=product_id)
        if not product_found:
            raise ProductNotFoundException(f"Product with id {product_id} not found")
        return await self.product_repository.increase_stock(product_id=product_id, quantity=quantity)

