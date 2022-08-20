from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    email: EmailStr = Field(sa_column_kwargs={"unique": True})
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=70)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)


class User(UserBase, table=True):
    hashed_password: str = Field(nullable=False)
