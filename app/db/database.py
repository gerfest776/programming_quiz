from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from app.config import get_config

engine = create_async_engine(
    get_config().db.ASYNC_DATABASE_URI,
    echo=True,
    future=True,
)


async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        autocommit=False, autoflush=False, bind=engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
