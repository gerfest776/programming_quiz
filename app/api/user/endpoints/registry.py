from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.user.deps.user import create_new_user
from app.db.database import get_session
from app.schemas.user import UserCreate, UserRead

router = APIRouter(prefix="/user")


@router.post("/create", response_model=UserRead)
async def create_user(
    new_user: UserCreate, session: AsyncSession = Depends(get_session)
):
    return await create_new_user(session, **new_user.dict())
