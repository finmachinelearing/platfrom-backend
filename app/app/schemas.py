import datetime
from typing import Optional, Dict
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


class CreateTask(BaseModel):

    short_description: str
    description: str
    start_date: str
    end_date: str
    function_id: int
    task_ans: Dict[str, str]
    ans_type: str


class Task(BaseModel):

    id: int
    short_description: str
    description: str
    start_date: datetime.datetime
    end_date: datetime.datetime
    function_id: int
    task_data: str
    task_ans: Dict[str, str]
    ans_type: str
    is_active: bool
