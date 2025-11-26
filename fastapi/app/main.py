from fastapi import FastAPI, HTTPException, Path, Body
from app.models import Product
from app.database import session, engine
from app.database import Base
from app.schemas import ProductCreate, ProductRead, GetSingleProductRequest

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
@app.get("/{product_id}", response_model=ProductRead)
def get_product_by_id(product_id: int = Path(..., description="The ID of the product to retrieve")):
    db = session()
    found_product = db.query(Product).filter(Product.id == product_id).first()
    if not found_product:
        raise HTTPException(status_code=404, detail="Product not found")
    print(found_product)
    return found_product

# create a new product
@app.post("/product", response_model=ProductRead)
def create_product(product: ProductCreate = Body(..., description="The product to create")):
    print(product)
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
@app.put("/product/{product_id}", response_model=ProductRead)
def update_product(product_id: int = Path(..., description="The ID of the product to update"), product: ProductCreate = Body(..., description="The updated product data")):
    db = session()
    existing_product = db.query(Product).filter(Product.id == product_id).first()
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")
    existing_product.name = product.name
    existing_product.price = product.price
    existing_product.description = product.description
    db.commit()
    db.refresh(existing_product)
    return existing_product

# delete a product
@app.delete("/product/{product_id}")
def delete_product(product_id: int = Path(..., description="The ID of the product to delete")):
    db = session()
    product  = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}

# search products by name
@app.get("/products/search")
def search_products(query: str):
    clean_query = query.strip().strip('"').strip("'") 
    db = session()
    products = db.query(Product).filter(Product.name.ilike(f"%{clean_query}%")).all()
    if not products:
        raise HTTPException(status_code=404, detail="No products found matching the query")
    return products

