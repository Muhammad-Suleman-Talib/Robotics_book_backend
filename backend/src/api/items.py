# This file will contain the API endpoints for item-related operations.
# For now, it's a placeholder.

from fastapi import APIRouter
from ..models.item import Item
from ..services import item_service

router = APIRouter()

@router.post("/items/", response_model=Item)
def create_item(item: Item):
    """
    Placeholder endpoint to create a new item.
    """
    return item_service.create_item(item=item)

@router.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    """
    Placeholder endpoint to retrieve an item by ID.
    """
    return item_service.get_item(item_id=item_id)
