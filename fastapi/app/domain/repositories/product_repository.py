from abc import ABC, abstractmethod
from typing import Optional
from app.domain.entities.product import Product
from app.domain.filters.product_filters import ProductSearchFilters

class ProductRepository(ABC):
    @abstractmethod
    async def get_products(self) -> tuple[list[Product], int]:
        pass

    @abstractmethod
    async def get_product_by_id(self, product_id: int) -> Optional[Product]:
        pass

    @abstractmethod
    async def get_product_by_name(self, name: str) -> Optional[Product]:
        pass

    @abstractmethod
    async  def create_product(self, product: Product) -> Product:
        pass

    @abstractmethod
    async def delete_product(self, product_id: int) -> Optional[Product]:
        pass

    @abstractmethod
    async def purchase_product(self, product_id: int, quantity: int) -> Optional[Product]:
        pass

    @abstractmethod
    async def increase_stock(self, product_id: int, quantity: int) -> Optional[Product]:
        pass

    @abstractmethod
    async def search_products(self, filters: ProductSearchFilters) -> tuple[list[Product], int]:
        pass