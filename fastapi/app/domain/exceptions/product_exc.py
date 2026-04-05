class ProductNotFoundException(Exception):
    pass

class ProductAlreadyExistsException(Exception):
    pass

class ProductOutofStockException(Exception):
    pass

class InsufficientStockException(Exception):
    pass

class DatabaseURLNotConfigured(Exception):
    pass