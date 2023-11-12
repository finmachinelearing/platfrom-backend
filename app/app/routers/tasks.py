import uuid
from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    UploadFile
)
from starlette.requests import Request
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from typing import Optional

from app.app.dependencies import get_db, get_s3
from app.app.schemas import CreateTask, EditTask
from app.app.utils import get_superadmin_or_404, get_current_user_id_or_403
from app.app.crud import (
    create_task_in_db,
    add_task_data_in_db,
    get_task_from_db,
    update_task_in_db,
    update_task_data_in_db,
    search_tasks_by_name_in_db,
    change_task_status_in_db
)
from app.app.config import S3_BUCKET_NAME

router = APIRouter(
    prefix='/tasks',
    tags=['Tasks']
)


@router.get('/search')
async def search_tasks(
        db: Session = Depends(get_db),
        _: int = Depends(get_current_user_id_or_403),
        name: Optional[str] = None,
        end_date: Optional[str] = None
):
    tasks = search_tasks_by_name_in_db(db=db, name=name, end_date=end_date)
    return tasks


@router.patch('/{task_id}/status')
async def change_task_status(
        task_id: int,
        db: Session = Depends(get_db),
        _: bool = Depends(get_superadmin_or_404),
):
    task = get_task_from_db(db=db, task_id=task_id)

    if not task:
        raise HTTPException(detail='Not found', status_code=404)

    change_task_status_in_db(db=db, task_id=task_id)

    return JSONResponse(content='Updated', status_code=200)


@router.post('/create')
async def create_task(
        request: Request,
        db: Session = Depends(get_db),
        _: bool = Depends(get_superadmin_or_404)
):
    request_data = await request.json()

    try:
        validated_request_data = CreateTask(**request_data)
    except ValidationError:
        raise HTTPException(detail='Request data is not valid', status_code=400)

    task = create_task_in_db(db=db, data=validated_request_data.model_dump())

    return JSONResponse(
        content={
            'task_id': task.id
        },
        status_code=201
    )


@router.post('/{task_id}/add_data')
async def add_task_data(
        file: UploadFile,
        task_id: int,
        db: Session = Depends(get_db),
        s3: Session = Depends(get_s3),
        _: bool = Depends(get_superadmin_or_404),
):
    try:
        file.file.read()
        file.file.seek(0)
        uid = str(uuid.uuid4())
        s3.upload_fileobj(file.file, S3_BUCKET_NAME, uid)
        add_task_data_in_db(db=db, task_id=task_id, uid=uid)
        return JSONResponse(content={'result': 'OK'}, status_code=201)
    except Exception:
        raise HTTPException(status_code=500, detail='Error on uploading the file')
    finally:
        file.file.close()


@router.get('/{task_id}')
async def get_task(
        task_id: int,
        db: Session = Depends(get_db),
        _: int = Depends(get_current_user_id_or_403)
):
    task = get_task_from_db(db=db, task_id=task_id)

    if not task:
        raise HTTPException(detail='Not found', status_code=404)

    return task


@router.patch('/{task_id}/update')
async def update_task(
        task_id: int,
        request: Request,
        db: Session = Depends(get_db),
        _: bool = Depends(get_superadmin_or_404),
):
    task = get_task_from_db(db=db, task_id=task_id)

    if not task:
        raise HTTPException(detail='Not found', status_code=404)

    request_data = await request.json()
    try:
        validated_request_data = EditTask(**request_data)
    except ValidationError:
        raise HTTPException(detail='Request data is not valid', status_code=400)

    fields_to_update = validated_request_data.model_dump(exclude_unset=True)
    update_task_in_db(db=db, task_id=task_id, fields_to_update=fields_to_update)

    return JSONResponse(content='Updated', status_code=200)


@router.patch('/{task_id}/update_data')
async def update_task_data(
        task_id: int,
        file: UploadFile,
        db: Session = Depends(get_db),
        s3: Session = Depends(get_s3),
        _: bool = Depends(get_superadmin_or_404),
):
    try:
        file.file.read()
        file.file.seek(0)
        uid = str(uuid.uuid4())
        s3.upload_fileobj(file.file, S3_BUCKET_NAME, uid)
        update_task_data_in_db(db=db, task_id=task_id, uid=uid)
        return JSONResponse(content='Updated', status_code=200)
    except Exception:
        raise HTTPException(status_code=500, detail='Error on uploading the file')
    finally:
        file.file.close()
