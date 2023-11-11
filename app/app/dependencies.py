from .database import SessionLocal
from .boto3 import s3


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_s3():
    return s3
