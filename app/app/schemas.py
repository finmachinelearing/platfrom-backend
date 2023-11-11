from typing import Optional
from pydantic import BaseModel


class User(BaseModel):

    provider_id: str
    name: str
    surname: str
    about: Optional[str] = None
    avatar_url: str
    email: str

    class Config:
        orm_mode = True


class TokenBlacklist(BaseModel):

    token: str


class EditUser(BaseModel):

    name: Optional[str] = None
    surname: Optional[str] = None
    about: Optional[str] = None


class Function(BaseModel):

    name: str
