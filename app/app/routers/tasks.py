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

from app.app.dependencies import get_db, get_s3
from app.app.schemas import CreateTask
from app.app.utils import get_superadmin_or_404
from app.app.crud import create_task_in_db, add_task_data_in_db
from app.app.config import S3_BUCKET_NAME

router = APIRouter(
    prefix='/tasks',
    tags=['Tasks']
)


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
