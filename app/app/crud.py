from sqlalchemy.orm import Session

from . import models
from . import schemas


def get_user(db: Session, provider_id: str):
    return db.query(models.User).filter(models.User.provider_id == provider_id).first()


def create_user(db: Session, user: schemas.User):
    db_user = models.User(
        provider_id=user.provider_id,
        name=user.name,
        surname=user.surname,
        about=user.about,
        avatar_url=user.avatar_url,
        email=user.email,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
