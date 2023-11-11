from typing import Dict
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


def ban_token(db: Session, token: schemas.TokenBlacklist):
    db_token = models.TokenBlacklist(
        token=token.token
    )
    db.add(db_token)
    db.commit()
    db.refresh(db_token)


def get_user_by_id(db: Session, user_id: int) -> models.User:
    return db.query(models.User).filter(models.User.id == user_id).first()


def update_user_in_db(
        db: Session,
        user_id: str,
        fields_to_update: Dict[str, str]
):
    user = get_user_by_id(db=db, user_id=user_id)

    for key, value in fields_to_update.items():
        setattr(user, key, value)

    db.add(user)
    db.commit()
    db.refresh(user)


def get_all_functions(db: Session):
    return db.query(models.Function).all()
