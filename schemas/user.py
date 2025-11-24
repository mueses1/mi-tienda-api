from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    email: str
    name: str
    role: str  # por ejemplo: "admin" o "customer"


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[str] = None
    name: Optional[str] = None
    role: Optional[str] = None
    password: Optional[str] = None


class UserInDB(UserBase):
    id: str

    class Config:
        from_attributes = True