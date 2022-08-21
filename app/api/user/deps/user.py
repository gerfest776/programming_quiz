from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.api.user.deps.auth import get_password_hash, verify_password
from app.db.models.user import User
from app.schemas.user import UserCreate


async def get_user(session: AsyncSession, user_id: User.id):
    return await session.get(User, int(user_id))


async def create_new_user(session: AsyncSession, **kwargs: UserCreate.dict):
    obj = User(**kwargs)
    obj.hashed_password = get_password_hash(obj.hashed_password)
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj


async def patch_exists_user(session: AsyncSession, user_id: User.id, **kwargs: UserCreate.dict):
    if user := get_user(session, user_id):
        for k, v in kwargs.items():
            setattr(user, k, v)

        await session.commit()
        await session.refresh(user)
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


async def authenticate(email: EmailStr | str, password: str, session: AsyncSession):
    user_qs = await session.execute(select(User).where(User.email == email))
    user = user_qs.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password")

    return user
