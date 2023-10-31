from abc import ABC
from typing import Generic, TypeVar, Callable, Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar('T')


class BaseAlchemyRepository(Generic[T], ABC):
    model: T = None

    def __init__(self, session_factory: Callable[[], AsyncSession]):
        self.session_factory = session_factory

    async def get_all(self) -> Sequence[T]:
        async with self.session_factory() as session:
            result = await session.execute(select(self.model))
            return result.scalars().all()

    async def get_by_id(self, id: UUID) -> T:
        async with self.session_factory() as session:
            result = await session.execute(select(self.model).where(self.model.id == id))
            return result.scalar_one()

    async def insert_one(self, instance: T) -> T:
        async with self.session_factory() as session:
            session.add(instance)
        return instance

    async def insert_many(self, objects: Sequence[T]) -> Sequence[T]:
        async with self.session_factory() as session:
            session.add_all(objects)
        return objects
