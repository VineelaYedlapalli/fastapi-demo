from fastapi import APIRouter, HTTPException
from app.models import Item
from typing import List

router = APIRouter(
    prefix="/items",
    tags=["Items"],
)

items_db: List[Item] = []
counter: int = 1


# ✅ GET all items
@router.get("/", response_model=List[Item])
def get_all_items():
    return items_db


# ✅ GET item by ID
@router.get("/{item_id}", response_model=Item)
def get_item(item_id: int):
    for item in items_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail=f"Item {item_id} not found")


# ✅ CREATE item (POST, not GET)
@router.post("/", response_model=Item, status_code=201)
def create_item(item: Item):
    global counter
    item.id = counter
    counter += 1
    items_db.append(item)
    return item