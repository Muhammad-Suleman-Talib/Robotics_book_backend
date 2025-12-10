# Placeholder for Item model tests.
# In a real application, you would test model validation, etc.

from backend.src.models.item import Item

def test_item_creation():
    item = Item(name="testitem", description="A test item.")
    assert item.name == "testitem"
    assert item.description == "A test item."
