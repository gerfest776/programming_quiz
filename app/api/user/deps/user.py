from app.db.models.user import UserDb
from app.schemas.user import UserCreate


async def create_new_user(**kwargs: UserCreate.dict):
    obj = UserDb(**kwargs)
