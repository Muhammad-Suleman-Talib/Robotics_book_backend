# This file will contain the API endpoints for user-related operations.
# For now, it's a placeholder.

from fastapi import APIRouter
from ..models.user import User
from ..services import user_service

router = APIRouter()

@router.post("/users/", response_model=User)
def create_user(user: User):
    """
    Placeholder endpoint to create a new user.
    """
    return user_service.create_user(user=user)

@router.get("/users/{user_id}", response_model=User)
def read_user(user_id: int):
    """
    Placeholder endpoint to retrieve a user by ID.
    """
    return user_service.get_user(user_id=user_id)
