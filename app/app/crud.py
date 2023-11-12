from typing import Dict, Any
from sqlalchemy import asc, text, desc
from sqlalchemy.orm import Session
from dateutil.parser import parse as parse_date
from typing import Optional

from . import models
from . import schemas
from app.app.sql_const import SCOREBOARD_SQL


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


def get_token(db: Session, token: str):
    return db.query(models.TokenBlacklist).filter(models.TokenBlacklist.token == token).first()


def create_task_in_db(db: Session, data: Dict[str, Any]):
    db_task = models.Task(
        name=data['name'],
        short_description=data['short_description'],
        description=data['description'],
        start_date=parse_date(data['start_date']),
        end_date=parse_date(data['end_date']),
        function_id=data['function_id'],
        task_ans=data['task_ans'],
        ans_type=data['ans_type'],
        tags=data['tags']
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_task_from_db(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def add_task_data_in_db(db: Session, task_id: int, uid: str):
    task = get_task_from_db(db=db, task_id=task_id)
    task.task_data = uid
    db.add(task)
    db.commit()
    db.refresh(task)


def update_task_in_db(
        db: Session,
        task_id: int,
        fields_to_update: Dict[str, str]
):
    task = get_task_from_db(db=db, task_id=task_id)

    for key, value in fields_to_update.items():
        setattr(task, key, value)

    db.add(task)
    db.commit()
    db.refresh(task)


def update_task_data_in_db(
        db: Session,
        task_id: int,
        uid: str
):
    task = get_task_from_db(db=db, task_id=task_id)
    task.task_data = uid
    db.add(task)
    db.commit()
    db.refresh(task)


def search_tasks_by_name_in_db(
        db: Session,
        name: Optional[str] = None,
        end_date: Optional[str] = None,
        tag: Optional[str] = None
):
    tasks = db.query(models.Task)

    if name:
        tasks = tasks.filter(models.Task.name.contains(name))

    if end_date:
        tasks = tasks.filter(models.Task.end_date <= parse_date(end_date))

    if tag:
        tasks = tasks.filter(models.Task.tags.contains([tag]))

    return tasks.filter(
        models.Task.is_active.is_(True)
    ).order_by(
        asc(models.Task.end_date)
    ).all()


def change_task_status_in_db(db: Session, task_id: int):
    task = get_task_from_db(db=db, task_id=task_id)
    task.is_active = not task.is_active
    db.add(task)
    db.commit()
    db.refresh(task)


def create_answer_in_db(
        db: Session,
        task_id: int,
        user_id: int,
        task_ans: Dict
):
    db_answer = models.Answer(
        task_id=task_id,
        user_id=user_id,
        task_ans=task_ans
    )
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer


def get_all_answers_for_task_in_db(db: Session, task_id: int):
    with db.connection() as conn:
        result = conn.execute(text(SCOREBOARD_SQL % {'task_id': task_id}))
        return result.all()


def get_user_answers_for_task_in_db(
        db: Session,
        task_id: int,
        user_id: int
):
    return db.query(
        models.Answer
    ).filter(
        models.Answer.task_id == task_id,
        models.Answer.user_id == user_id,
        models.Answer.score.is_not(None),
        models.Answer.is_active.is_(True)
    ).order_by(
        desc(models.Answer.added_at)
    ).all()
