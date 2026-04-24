from fastapi import APIRouter, HTTPException, Response
from app.models import Item
from typing import List

router = APIRouter(
    prefix="/items",
    tags=["Items"],
)

items_db: List[Item] = []
counter: int = 1


@router.get("/", response_model=List[Item])
def get_all_items():
    return items_db


@router.get("/{item_id}", response_model=Item)
def get_item(item_id: int):
    for item in items_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail=f"Item {item_id} not found")


@router.post("/", response_model=Item, status_code=201)
def create_item(item: Item):
    global counter
    item.id = counter
    counter += 1
    items_db.append(item)
    return item


@router.put("/{item_id}", response_model=Item)
def update_item(item_id: int, updated_item: Item):
    for index, item in enumerate(items_db):
        if item.id == item_id:
            updated_item.id = item_id
            items_db[index] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail=f"Item with id {item_id} not found")


@router.delete("/{item_id}", status_code=204)
def delete_item(item_id: int):
    for index, item in enumerate(items_db):
        if item.id == item_id:
            items_db.pop(index)
            return Response(status_code=204)
    raise HTTPException(status_code=404, detail=f"Item with id {item_id} not found")