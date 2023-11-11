import json
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import DATABASE_MAX_POOL, DATABASE_URL, DATABASE_MAX_OVERFLOW


def dumps(d):
    return json.dumps(d, ensure_ascii=False)


engine = create_engine(
    DATABASE_URL,
    pool_size=DATABASE_MAX_POOL,
    max_overflow=DATABASE_MAX_OVERFLOW,
    json_serializer=dumps
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
