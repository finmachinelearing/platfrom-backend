from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    DateTime,
    ForeignKey,
    JSON
)
from sqlalchemy_utils import EmailType
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    provider_id = Column(String, index=True)
    name = Column(String)
    surname = Column(String)
    about = Column(Text, nullable=True, default=None)
    avatar_url = Column(String)
    is_active = Column(Boolean, default=True)
    email = Column(EmailType)
    is_superuser = Column(Boolean, default=False)
    joined_date = Column(DateTime, default=datetime.now)


class TokenBlacklist(Base):

    __tablename__ = 'token_blacklist'

    id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(String)


class Task(Base):

    __tablename__ = 'task'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    short_description = Column(Text)
    description = Column(Text)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    function_id = Column(Integer, ForeignKey('function.id'))
    task_data = Column(String, nullable=True, default=None)
    task_ans = Column(JSON)
    ans_type = Column(String)
    is_active = Column(Boolean, default=False)

    function = relationship('Function', back_populates='task')


class Function(Base):

    __tablename__ = 'function'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    task = relationship('Task', back_populates='function')
