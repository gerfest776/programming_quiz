from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.db.models.user import User
from app.schemas.user import UserCreate


async def create_new_user(session: AsyncSession, **kwargs: UserCreate.dict):
    obj = User(**kwargs)
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj


async def patch_exists_user(
    session: AsyncSession, user_id: User.id, **kwargs: UserCreate.dict
):
    if user := await session.get(User, user_id):
        for k, v in kwargs.items():
            setattr(user, k, v)

        await session.commit()
        await session.refresh(user)
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
