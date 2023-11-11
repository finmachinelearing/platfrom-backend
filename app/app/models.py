from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    DateTime
)
from sqlalchemy_utils import EmailType

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
