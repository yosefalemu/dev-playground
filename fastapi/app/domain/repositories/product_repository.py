from abc import ABC, abstractmethod
from typing import Optional, Protocol
from app.domain.entities.product import Product

class ProductRepository(ABC):
    @abstractmethod
    def get_products(self) -> list[Product]:
        pass

    @abstractmethod
    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        pass

    @abstractmethod
    def get_product_by_name(self, name: str) -> Optional[Product]:
        pass

    @abstractmethod
    def create_product(self, product: Product) -> Product:
        pass

    @abstractmethod
    def delete_product(self, product_id: int) -> Optional[Product]:
        pass

    @abstractmethod
    def purchase_product(self, product_id: int, quantity: int) -> Product:
        pass

    @abstractmethod
    def increase_stock(self, product_id: int, quantity: int) -> Product:
        pass