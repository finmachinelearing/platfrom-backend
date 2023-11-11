from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from starlette.requests import Request
from sqlalchemy.orm import Session
from fastapi_sso.sso.google import GoogleSSO
from oauthlib.oauth2.rfc6749.errors import InvalidGrantError

from app.app.schemas import User, TokenBlacklist
from app.app.crud import get_user, create_user, ban_token
from app.app.dependencies import get_db
from app.app.utils import (
    create_access_token,
    create_refresh_token,
    get_current_user_id_or_403,
    get_refresh_token_or_403
)
from app.app.config import (
    DEBUG,
    GOOGLE_SSO_CLIENT_ID,
    GOOGLE_SSO_CLIENT_SECRET,
    GOOGLE_CALLBACK,
    REFRESH_TOKEN_EXPIRE_MINUTES
)

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)

sso = GoogleSSO(
    client_id=GOOGLE_SSO_CLIENT_ID,
    client_secret=GOOGLE_SSO_CLIENT_SECRET,
    redirect_uri=GOOGLE_CALLBACK,
    allow_insecure_http=DEBUG
)


@router.get('/google/login')
async def mail_sso_login():
    return await sso.get_login_redirect()


@router.get('/google/callback')
async def google_sso_callback(request: Request, db: Session = Depends(get_db)):
    try:
        user = await sso.verify_and_process(request)
    except InvalidGrantError:
        raise HTTPException(detail='Bad request', status_code=400)

    provider_id = str(user.id)
    db_user = get_user(db=db, provider_id=provider_id)

    if not db_user:
        db_user = create_user(
            db=db,
            user=User(
                provider_id=provider_id,
                name=user.first_name,
                surname=user.last_name,
                avatar_url=user.picture,
                email=user.email
            )
        )

    response = JSONResponse(
        content={
            'access_token': create_access_token(db_user)
        },
        status_code=200
    )

    response.set_cookie(
        key='refresh_token',
        value=create_refresh_token(db_user),
        httponly=True,
        max_age=REFRESH_TOKEN_EXPIRE_MINUTES * 60
    )

    return response


@router.post('/logout')
async def logout(
    db: Session = Depends(get_db),
    _: int = Depends(get_current_user_id_or_403),
    refresh_token: str = Depends(get_refresh_token_or_403)
):
    ban_token(
        db=db,
        token=TokenBlacklist(
            token=refresh_token
        )
    )
    return JSONResponse(content={'result': 'OK'}, status_code=200)
