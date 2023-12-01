from datetime import datetime
from typing import Optional, Dict, List
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


class ReturnUser(User):

    joined_date: datetime


class TokenBlacklist(BaseModel):

    token: str


class EditUser(BaseModel):

    name: Optional[str] = None
    surname: Optional[str] = None
    about: Optional[str] = None


class Function(BaseModel):

    name: str


class CreateTask(BaseModel):

    name: str
    short_description: str
    description: str
    start_date: str
    end_date: str
    function_id: int
    task_ans: Dict[str, str]
    ans_type: str
    tags: List[str]


class EditTask(BaseModel):

    name: Optional[str] = None
    short_description: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    function_id: Optional[int] = None
    task_ans: Optional[Dict[str, str]] = None
    ans_type: Optional[str] = None
    is_active: Optional[bool] = None
    tags: Optional[List[str]] = None


class ReturnTask(BaseModel):

    id: int
    name: str
    short_description: str
    description: str
    start_date: datetime
    end_date: datetime
    function_id: int
    task_data: Optional[str]
    ans_type: str
    tags: Optional[List[str]]
    is_active: bool
