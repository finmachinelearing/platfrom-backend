from fastapi import FastAPI

from .config import DEBUG
from .routers import auth, user
from .database import engine
from . import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

if not DEBUG:
    app = FastAPI(docs_url=None, redoc_url=None)

app.include_router(router=auth.router)
app.include_router(router=user.router)
