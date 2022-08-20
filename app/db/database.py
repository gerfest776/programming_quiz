from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declarative_base

from app.config import get_config

engine = create_engine(
    url=get_config().db.dsn, connect_args={"check_same_thread": False}
)

session = AsyncSession(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


async def get_session() -> AsyncSession:
    try:
        yield session
    finally:
        await session.close()
