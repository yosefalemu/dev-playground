from app.domain.entities.product import Product

class ProductListResponseDTO:
    def __init__(self, products: list[Product], count: int):
        self.products = products
        self.count = count