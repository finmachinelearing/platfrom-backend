import json
from datetime import datetime, timedelta
from typing import Any, Union
from jose import jwt
from fastapi import HTTPException, Request
from jose.exceptions import ExpiredSignatureError, JWTError

from .config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    JWT_SECRET_KEY,
    ALGORITHM,
    REFRESH_TOKEN_EXPIRE_MINUTES,
    JWT_REFRESH_SECRET_KEY
)


def dumps(d):
    return json.dumps(d, ensure_ascii=False)


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
