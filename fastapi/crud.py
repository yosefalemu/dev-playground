from fastapi import APIRouter
import model as model_module

router = APIRouter()
items: list[model_module.Item] = []

@router.get("/items/")
async def get_items():
    if len(items) == 0:
        return {"message": "No items are found!"}
    return {"message": "Items are retrieved!", "data": items}

@router.get("/items/{item_id}")
async def get_item(item_id: int):
    try:
        selected_item = items[item_id - 1]
    except IndexError:
        return {"message": f"Item with id {item_id} is not found!"}
    return {"message": f"Item with id {item_id} is retrieved!", "data": selected_item}

@router.post("/items/")
async def create_item(item: model_module.Item):
    item_id = len(items) + 1
    item.id = item_id
    items.append(item)
    return {"message": f"Item with id {item_id} is created!", "data": item}

@router.put("/items/{item_id}")
async def update_item(item_id: int, item:model_module.Item):
    try:
        selected_item = items[item_id - 1]
    except IndexError:
         return {"message": f"Item with id {item_id} is not found!"}
    selected_item.name = item.name
    selected_item.description = item.description
    selected_item.price = item.price
    selected_item.tax = item.tax
    return {"message": f"Item with id {item_id} is updated!", "data": selected_item}

@router.delete("/items/{item_id}")
async def delete_item(item_id: int):
    try:
         selected_item = items[item_id - 1]
    except IndexError:
         return {"message": f"Item with id {item_id} is not found!"}
    items.remove(selected_item)
    return {"message": f"Item with id {item_id} is deleted!"}
