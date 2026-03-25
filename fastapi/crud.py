from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import model, schemas
from database import engine, get_db
# import model as model_module

model.Base.metadata.create_all(bind=engine)
router = APIRouter()
# items: list[model_module.Item] = []

@router.get("/items/", response_model=list[schemas.ItemBase])
async def get_items(skip: int = 0, limit:int = 100, db: Session = Depends(get_db)):
    items = db.query(model.Item).offset(skip).limit(limit).all()
    if len(items) == 0:
        raise HTTPException(status_code=404, detail="No items found!")
    return items

@router.get("/items/{item_id}", response_model=schemas.ItemBase)
async def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(model.Item).filter(model.Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail=f"Item with id {item_id} is not found!")
    return item

@router.post("/items/", response_model=schemas.ItemBase)
async def create_item(item: schemas.ItemBase, db: Session = Depends(get_db)):
    new_item = model.Item(**item.model_dump())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

# @router.put("/items/{item_id}")
# async def update_item(item_id: int, item:model_module.Item):
#     try:
#         selected_item = items[item_id - 1]
#     except IndexError:
#          return {"message": f"Item with id {item_id} is not found!"}
#     selected_item.name = item.name
#     selected_item.description = item.description
#     selected_item.price = item.price
#     selected_item.tax = item.tax
#     return {"message": f"Item with id {item_id} is updated!", "data": selected_item}

# @router.delete("/items/{item_id}")
# async def delete_item(item_id: int):
#     try:
#          selected_item = items[item_id - 1]
#     except IndexError:
#          return {"message": f"Item with id {item_id} is not found!"}
#     items.remove(selected_item)
#     return {"message": f"Item with id {item_id} is deleted!"}
