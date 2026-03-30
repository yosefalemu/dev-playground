from abc import ABC, abstractmethod
from typing import Optional, Protocol
from app.domain.entities.product import Product

class ProductRepository(ABC):
    @abstractmethod
    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        pass

    @abstractmethod
    def save_product(self, product: Product) -> None:
        pass