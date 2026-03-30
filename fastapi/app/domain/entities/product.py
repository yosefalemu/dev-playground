class Product:
    def __init__ (self, id: int, name: str, stock: int, price: float):
        self.id = id
        self.name = name
        self.stock = stock
        self.price = price
    def check_stock(self, quantity: int) -> bool:
        return self.stock >= quantity
    def reduce_stock(self, quantity: int):
        if self.check_stock(quantity):
            self.stock -= quantity
        else:
            raise ValueError("Not enough stock available")
    def increase_stock(self, quantity: int):
        self.stock += quantity