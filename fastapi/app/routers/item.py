import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models, schemas
from database import engine, get_db
from app.dependencies import get_token_header, get_query_token

models.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(get_token_header), Depends(get_query_token)]
)

@router.get("/", response_model=list[schemas.ItemBase], description="Get a list of items with pagination support.")
async def get_items(skip: int = 0, limit:int = 100, db: Session = Depends(get_db)):
    items = db.query(models.Item).offset(skip).limit(limit).all()
    if len(items) == 0:
        raise HTTPException(status_code=404, detail="No items found!")
    return items

@router.get("/{item_id}", response_model=schemas.ItemBase, description="Get an item by its ID.")
async def get_item(item_id: uuid.UUID, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail=f"Item with id {item_id} is not found!")
    return item

@router.post("/", response_model=schemas.ItemBase, description="Create a new item.")
async def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    new_item = models.Item(**item.model_dump())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

@router.put("/{item_id}", response_model=schemas.ItemBase, description="Update an existing item.")
async def update_item(item_id: uuid.UUID, item: schemas.ItemUpdate, db: Session = Depends(get_db)):
    selected_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if selected_item is None:
        raise HTTPException(status_code=404, detail=f"Item with id {item_id} is not found!")
    for key, value in item.model_dump().items():
        if value is not None:
            setattr(selected_item, key, value)
    db.commit()
    db.refresh(selected_item)
    return selected_item

@router.delete("/{item_id}", description="Delete an existing item.")
async def delete_item(item_id: uuid.UUID, db: Session = Depends(get_db)):
    selected_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if selected_item is None:
        raise HTTPException(status_code=404, detail=f"Item with id {item_id} is not found!")
    db.delete(selected_item)
    db.commit()
    return {"message": f"Item with id {item_id} is deleted!"}

