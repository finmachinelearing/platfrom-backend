from fastapi import FastAPI, HTTPException
from starlette.requests import Request
from fastapi_sso.sso.base import DiscoveryDocument
from fastapi_sso.sso.generic import create_provider

from .config import DEBUG, MAIL_SSO_CLIENT_ID, MAIL_SSO_CLIENT_SECRET
from .database import engine
from . import models
from .utils import convert_openid

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

if not DEBUG:
    app = FastAPI(docs_url=None, redoc_url=None)

discovery_document: DiscoveryDocument = {
    'authorization_endpoint': 'https://oauth.mail.ru/login',
    'token_endpoint': 'https://oauth.mail.ru/token',
    'userinfo_endpoint': 'https://oauth.mail.ru/userinfo',
}

MailSSO = create_provider(
    name='Mail',
    discovery_document=discovery_document,
    response_convertor=convert_openid
)

mail_sso = MailSSO(
    client_id=MAIL_SSO_CLIENT_ID,
    client_secret=MAIL_SSO_CLIENT_SECRET,
    redirect_uri='http://localhost:8000/auth/mail/callback',
    allow_insecure_http=True
)


@app.get('/')
async def root():
    return {'message': 'Hello World'}


@app.get('/auth/mail/login')
async def mail_sso_login():
    with mail_sso:
        return await mail_sso.get_login_redirect()


@app.get('/auth/mail/callback')
async def mail_sso_callback(request: Request):
    with mail_sso:
        user = await mail_sso.verify_and_process(request)

    if not user:
        raise HTTPException(401, 'Failed to fetch user information')

    return user
