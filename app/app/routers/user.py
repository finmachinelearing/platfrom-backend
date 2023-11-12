from fastapi import APIRouter, HTTPException, Depends
from starlette.requests import Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import ValidationError

from app.app.dependencies import get_db
from app.app.utils import get_current_user_id_or_403
from app.app.schemas import User, EditUser
from app.app.crud import get_user_by_id, update_user_in_db

router = APIRouter(
    prefix='/user',
    tags=['USer']
)


@router.get('/{user_id}', response_model=User)
async def get_user(
        db: Session = Depends(get_db),
        user_id: int = Depends(get_current_user_id_or_403)
):
    user = get_user_by_id(db=db, user_id=user_id)

    if not user:
        raise HTTPException(detail='Not found', status_code=404)

    return user


@router.patch('/{user_id}/update')
async def update_user(
        request: Request,
        db: Session = Depends(get_db),
        user_id: int = Depends(get_current_user_id_or_403)
):
    user = get_user_by_id(db=db, user_id=user_id)

    if not user:
        raise HTTPException(detail='Not found', status_code=404)

    request_data = await request.json()
    try:
        validated_request_data = EditUser(**request_data)
    except ValidationError:
        raise HTTPException(detail='Request data is not valid', status_code=400)

    fields_to_update = validated_request_data.model_dump(exclude_unset=True)
    update_user_in_db(db=db, user_id=user_id, fields_to_update=fields_to_update)

    return JSONResponse(content='Updated', status_code=200)
