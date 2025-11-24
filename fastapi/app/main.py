from fastapi import FastAPI, Depends
from app.models import Product
from app.database import session, engine
from app.database import Base
from app.schemas import ProductCreate

app = FastAPI()

# Create tables
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Hello World"}




# get all products
@app.get("/products")
def get_products():
    db = session()
    products = db.query(Product).all()
    return products


# get a product by id
# @app.get("/products/{product_id}")
# def get_product(product_id: int):
#     product = next((p for p in products if p.id == product_id), None)
#     if product:
#         return product
#     else:
#         raise HTTPException(status_code=404, detail="Product not found")


# create a new product
@app.post("/product", response_model=ProductCreate)
def create_product(product: ProductCreate):
    db = session()
    db_product = Product(
        name=product.name,
        price=product.price,
        description=product.description
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product



# update a product
# @app.put("/products/{product_id}")
# def update_product(product_id: int, updated_product: Product):
#     product = next((p for p in products if p.id == product_id), None)
#     if product:
#         product.name = updated_product.name
#         product.price = updated_product.price
#         product.description = updated_product.description
#         return product
#     else:
#         raise HTTPException(status_code=404, detail="Product not found")


# delete a product
# @app.delete("/products/{product_id}")
# def delete_product(product_id: int):
#     product = next((p for p in products if p.id == product_id), None)
#     if product:
#         products.remove(product)
#         return {"message": "Product deleted successfully"}
#     else:
#         raise HTTPException(status_code=404, detail="Product not found")

# @app.get("/products/search")
# def search_products(query:str):
#     product = next((p for p in products if query in p.name),None)
#     if product:
#         return product
#     else:
#         raise HTTPException(status_code=404, detail="Product not found")
