import csv
from io import StringIO
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
from app.app.schemas import CreateTask, EditTask, ReturnTask
from app.app.utils import get_superadmin_or_404
from app.app.crud import (
    create_task_in_db,
    add_task_data_in_db,
    get_task_from_db,
    update_task_in_db,
    update_task_data_in_db,
    search_tasks_by_name_in_db,
    change_task_status_in_db,
    get_user_by_id,
    get_all_tasks_for_user_id_db,
    add_task_answer_in_db,
    update_task_answer_in_db,
    add_test_data_in_db,
    update_test_data_in_db
)
from app.app.config import S3_BUCKET_NAME

router = APIRouter(
    prefix='/tasks',
    tags=['Tasks']
)


@router.get('/search', response_model=list[ReturnTask])
async def search_tasks(
        db: Session = Depends(get_db),
        s3: Session = Depends(get_s3),
        name: Optional[str] = None,
        end_date: Optional[str] = None,
        tag: Optional[str] = None
):
    tasks = search_tasks_by_name_in_db(
        db=db,
        name=name,
        end_date=end_date,
        tag=tag
    )

    for task in tasks:
        task_data = task.task_data
        test_data = task.test_data

        if task_data:
            task.task_data = s3.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': S3_BUCKET_NAME,
                    'Key': task_data
                },
                ExpiresIn=1800
            )

        if test_data:
            task.test_data = s3.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': S3_BUCKET_NAME,
                    'Key': test_data
                },
                ExpiresIn=1800
            )

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


@router.post('/{task_id}/add_test_data')
async def add_test_data(
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
        add_test_data_in_db(db=db, task_id=task_id, uid=uid)
        return JSONResponse(content={'result': 'OK'}, status_code=201)
    except Exception:
        raise HTTPException(status_code=500, detail='Error on uploading the file')
    finally:
        file.file.close()


@router.post('/{task_id}/add_answer')
async def add_task_answer(
        file: UploadFile,
        task_id: int,
        db: Session = Depends(get_db),
        _: bool = Depends(get_superadmin_or_404),
):
    task = get_task_from_db(db=db, task_id=task_id)

    if not task:
        raise HTTPException(detail='Task not found', status_code=404)

    try:
        csv_reader = csv.reader(StringIO(file.file.read().decode()), delimiter=',')
        csv_data = list(csv_reader)
    except Exception:
        raise HTTPException(detail='CSV is not correct', status_code=400)

    task_ans = {}

    for row in csv_data[1:]:
        id, result = row
        task_ans[id] = result.strip()

    add_task_answer_in_db(db=db, task_id=task_id, task_ans=task_ans)
    return JSONResponse(content={'result': 'OK'}, status_code=201)


@router.get('/{task_id}', response_model=ReturnTask)
async def get_task(
        task_id: int,
        db: Session = Depends(get_db),
        s3: Session = Depends(get_s3)
):
    task = get_task_from_db(db=db, task_id=task_id)

    if not task:
        raise HTTPException(detail='Not found', status_code=404)

    task_data = task.task_data
    test_data = task.test_data

    if task_data:
        task.task_data = s3.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': S3_BUCKET_NAME,
                'Key': task_data
            },
            ExpiresIn=1800
        )

    if test_data:
        task.test_data = s3.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': S3_BUCKET_NAME,
                'Key': test_data
            },
            ExpiresIn=1800
        )

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


@router.patch('/{task_id}/update_test_data')
async def update_test_data(
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
        update_test_data_in_db(db=db, task_id=task_id, uid=uid)
        return JSONResponse(content='Updated', status_code=200)
    except Exception:
        raise HTTPException(status_code=500, detail='Error on uploading the file')
    finally:
        file.file.close()


@router.patch('/{task_id}/update_answer')
async def update_task_answer(
        file: UploadFile,
        task_id: int,
        db: Session = Depends(get_db),
        _: bool = Depends(get_superadmin_or_404),
):
    task = get_task_from_db(db=db, task_id=task_id)

    if not task:
        raise HTTPException(detail='Task not found', status_code=404)

    try:
        csv_reader = csv.reader(StringIO(file.file.read().decode()), delimiter=',')
        csv_data = list(csv_reader)
    except Exception:
        raise HTTPException(detail='CSV is not correct', status_code=400)

    task_ans = {}

    for row in csv_data[1:]:
        id, result = row
        task_ans[id] = result.strip()

    update_task_answer_in_db(db=db, task_id=task_id, task_ans=task_ans)
    return JSONResponse(content='Updated', status_code=200)


@router.get('/participant/{user_id}', response_model=list[ReturnTask])
async def get_all_tasks_for_user(
        user_id: int,
        db: Session = Depends(get_db),
        s3: Session = Depends(get_s3)
):
    user = get_user_by_id(db=db, user_id=user_id)

    if not user:
        raise HTTPException(detail='User not found', status_code=404)

    tasks = get_all_tasks_for_user_id_db(db=db, user_id=user_id)

    for task in tasks:
        task_data = task.task_data
        test_data = task.test_data

        if task_data:
            task.task_data = s3.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': S3_BUCKET_NAME,
                    'Key': task_data
                },
                ExpiresIn=1800
            )

        if test_data:
            task.test_data = s3.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': S3_BUCKET_NAME,
                    'Key': test_data
                },
                ExpiresIn=1800
            )

    return tasks
