from datetime import datetime, timedelta
from typing import Any, Union
from jose import jwt
from fastapi import HTTPException, Request, Depends
from jose.exceptions import ExpiredSignatureError, JWTError
from sqlalchemy.orm import Session

from .dependencies import get_db
from .crud import get_user_by_id
from .config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    JWT_SECRET_KEY,
    ALGORITHM,
    REFRESH_TOKEN_EXPIRE_MINUTES,
    JWT_REFRESH_SECRET_KEY
)


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {
        'exp': expires_delta,
        'sub': str(subject),
        'avatar_url': subject.avatar_url,
        'user_id': subject.id,
        'name': subject.name,
        'surname': subject.surname
    }
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = {
        'exp': expires_delta,
        'sub': str(subject),
        'user_id': subject.id
    }
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt


def get_current_user_id_or_403(request: Request) -> int:
    access_token = request.headers.get('authorization')

    if not access_token:
        raise HTTPException(status_code=403, detail='Unauthorized')

    try:
        claims = jwt.decode(access_token.split()[1], JWT_SECRET_KEY)
    except (JWTError, ExpiredSignatureError):
        raise HTTPException(status_code=403, detail='Unauthorized')

    return claims.get('user_id')


def get_refresh_token_or_403(request: Request) -> str:
    refresh_token = request.cookies.get('refresh_token')

    if not refresh_token:
        raise HTTPException(status_code=403, detail='Unauthorized')

    try:
        jwt.decode(refresh_token, JWT_REFRESH_SECRET_KEY)
    except (JWTError, ExpiredSignatureError):
        raise HTTPException(status_code=403, detail='Unauthorized')

    return refresh_token


def get_superadmin_or_404(request: Request, db: Session = Depends(get_db)) -> bool:
    access_token = request.headers.get('authorization')

    if not access_token:
        raise HTTPException(status_code=404, detail='Not Found')

    try:
        claims = jwt.decode(access_token.split()[1], JWT_SECRET_KEY)
        user_id = claims.get('user_id')
    except (JWTError, ExpiredSignatureError):
        raise HTTPException(status_code=404, detail='Not Found')

    user = get_user_by_id(db=db, user_id=user_id)

    if user.is_superuser:
        return True

    raise HTTPException(status_code=404, detail='Not Found')


def get_user_id_from_refresh_token(refresh_token: str) -> int:
    claims = jwt.decode(refresh_token, JWT_REFRESH_SECRET_KEY)
    return claims.get('user_id')
