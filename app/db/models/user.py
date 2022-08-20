from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    email: EmailStr = Field(primary_key=True)
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=70)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    hashed_password: str = Field(nullable=False)
