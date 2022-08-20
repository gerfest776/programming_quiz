from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User
from app.schemas.user import UserCreate


async def create_new_user(session: AsyncSession, **kwargs: UserCreate.dict):
    obj = User(**kwargs)
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj
