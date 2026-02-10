from fastapi import Body, APIRouter
from typing import List

from app.models.users import UserCreate, UserUpdate, UserOut
from app.services import users as user_services


router = APIRouter(
    tags=["Users"],
    prefix="/users",
    responses={404: {"description": "Not found"}}
)


@router.get('/', response_model=List[UserOut])
async def get_all_users():
    """Get all users."""
    return await user_services.get_all_users()


@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: int):
    """Get user by ID."""
    return await user_services.get_user(user_id=user_id)


@router.post('/', status_code=201, response_model=UserOut)
async def create_user(user: UserCreate = Body(...)):
    """Create a new user."""
    return await user_services.create_user(user_data=user.model_dump())


@router.put('/{user_id}', response_model=UserOut)
async def update_user(user_id: int, user: UserUpdate = Body(...)):
    """Update an existing user."""
    return await user_services.update_user(user_id=user_id, user_data=user.model_dump())


@router.delete('/{user_id}')
async def delete_user(user_id: int):
    """Delete a user."""
    return await user_services.delete_user(user_id=user_id)
