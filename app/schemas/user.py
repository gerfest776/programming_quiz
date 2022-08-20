from pydantic import BaseModel, EmailStr

from app.db.models.user import UserBase


class UserCreate(BaseModel):
    email: EmailStr
    hashed_password: str
    first_name: str
    last_name: str


class UserRead(UserBase):
    id: int
