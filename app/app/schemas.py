from typing import Optional
from pydantic import BaseModel


class User(BaseModel):

    provider_id: str
    name: str
    surname: str
    about: Optional[str]
    avatar_url: str
    email: str

    class Config:
        orm_mode = True
