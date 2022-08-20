from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.user.deps.user import create_new_user, patch_exists_user
from app.db.database import get_session
from app.schemas.user import UserCreate, UserPatch, UserRead

router = APIRouter(prefix="/user")


@router.post("/", response_model=UserRead)
async def create_user(
    new_user: UserCreate, session: AsyncSession = Depends(get_session)
):
    return await create_new_user(session, **new_user.dict())


@router.patch("/{user_id}", response_model=UserRead)
async def patch_user(
    user_id: int,
    patch_data: UserPatch,
    session: AsyncSession = Depends(get_session),
):
    return await patch_exists_user(session, user_id, **patch_data.dict())
