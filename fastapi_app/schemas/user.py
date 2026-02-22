# fastapi-app/schemas/user.py
from pydantic import BaseModel, Field

class UserBase(BaseModel):
    username: str = Field(..., min_length=1)

class UserCreate(UserBase):
    password: str = Field(..., min_length=4)
    role: str = Field(default="user")  # デフォルトは "user"

class UserLogin(UserBase):
    password: str = Field(..., min_length=4)

class UserResponse(UserBase):
    id: int
    role: str

    class Config:
        from_attributes = True  # ORM モード
