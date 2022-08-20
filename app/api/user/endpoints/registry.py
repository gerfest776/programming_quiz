from fastapi import APIRouter

from app import db
from app.api.user.deps.user import create_new_user
from app.schemas.user import UserCreate, UserRead

router = APIRouter(prefix="user")


@router.post("/create", response_model=UserRead)
async def create_user(new_user: UserCreate):
    new_user = await create_new_user(**new_user.dict())
