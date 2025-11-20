from fastapi import FastAPI, HTTPException
from models import Product

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello World"}


products = [
    Product(id=1, name="Product 1", price=100, description="Description 1"),
    Product(id=2, name="Product 2", price=200, description="Description 2"),
    Product(id=3, name="Product 3", price=300, description="Description 3"),
]


# get all products
@app.get("/products")
def get_products():
    return products


# get a product by id
@app.get("/products/{product_id}")
def get_product(product_id: int):
    product = next((p for p in products if p.id == product_id), None)
    if product:
        return product
    else:
        raise HTTPException(status_code=404, detail="Product not found")


# create a new product
@app.post("/product")
def create_product(product: Product):
    products.append(product)
    return product


# update a product
@app.put("/products/{product_id}")
def update_product(product_id: int, updated_product: Product):
    product = next((p for p in products if p.id == product_id), None)
    if product:
        product.name = updated_product.name
        product.price = updated_product.price
        product.description = updated_product.description
        return product
    else:
        raise HTTPException(status_code=404, detail="Product not found")


# delete a product
@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    product = next((p for p in products if p.id == product_id), None)
    if product:
        products.remove(product)
        return {"message": "Product deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Product not found")

@app.get("/products/search")
def search_products(query:str):
    product = next((p for p in products if query in p.name),None)
    if product:
        return product
    else:
        raise HTTPException(status_code=404, detail="Product not found")
