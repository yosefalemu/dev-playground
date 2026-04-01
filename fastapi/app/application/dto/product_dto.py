class ProductResponseDTO:
    def __init__(self, id: int, name: str, stock: int,price: float):
        self.id = id
        self.name = name
        self.stock = stock
        self.price = price
class ProductResponseForUserDTO:
    def __init__(self, id: int, name: str, price: float):
        self.id = id
        self.name = name
        self.price = price
class ProductListResponseDTO:
    def __init__(self, products: list[ProductResponseForUserDTO], count: int):
        self.products = products
        self.count = count