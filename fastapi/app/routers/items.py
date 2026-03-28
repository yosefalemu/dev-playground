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
    dependencies=[Depends(get_token_header), Depends(get_query_token)],
)

@router.get("/", 
            response_model=schemas.ItemResponse, 
            description="Get a list of items with pagination support.", 
            responses={404: {"description": "No items found!", "content": {"application/json": {"example": {"detail": "No items found!"}}}}})
async def get_items(skip: int = 0, limit:int = 100, db: Session = Depends(get_db)):
    items = db.query(models.Item).offset(skip).limit(limit).all()
    if len(items) == 0:
        raise HTTPException(status_code=404, detail="No items found!")
    return {"data": items, "total": len(items)}

@router.get("/{item_id}", 
            response_model=schemas.ItemBase, 
            description="Get an item by its ID.", 
            responses={404: {"description": f"Item with id {{item_id}} is not found!", "content": {"application/json": {"example": {"detail": f"Item with id {{item_id}} id not found!"}}}}})
async def get_item(item_id: uuid.UUID, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail=f"Item with id {item_id} is not found!")
    return item

@router.post("/", 
             response_model=schemas.ItemBase, 
             description="Create a new item.",
             responses={400: {"description": "Invalid item  data!", "content": {"application/json": {"example": {"detail": "Invalid item data!"}}}}})
async def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    new_item = models.Item(**item.model_dump())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

@router.put("/{item_id}", 
            response_model=schemas.ItemBase, 
            description="Update an existing item.",
            responses={
                400 : {"description": "Invalid item data!", "content": {"application/json": {"example": {"detail": "Invalid item data!"}}}},
                404: {"description": f"Item with id {{item_id}} is not found!", "content": {"application/json": {"example":{"detail": f"Item with id {{item_id}} is not found!"}}}}})
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

@router.delete("/{item_id}", 
               response_model=schemas.ItemBase, 
               description="Delete an existing item.",
               responses={404: {"description": f"item with id {{item_id}} is not found!", "content": {"application/json":{"example": {"detail": f"Item with id {{item_id}} is not found!"}}}}})
async def delete_item(item_id: uuid.UUID, db: Session = Depends(get_db)):
    selected_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if selected_item is None:
        raise HTTPException(status_code=404, detail=f"Item with id {item_id} is not found!")
    db.delete(selected_item)
    db.commit()
    return selected_item

