import csv
from io import StringIO
from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    UploadFile
)
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from csvvalidator import CSVValidator

from app.app.dependencies import get_db
from app.app.utils import get_current_user_id_or_403, check_csv_records
from app.app.crud import (
    create_answer_in_db,
    get_all_answers_for_task_in_db,
    get_user_answers_for_task_in_db
)

router = APIRouter(
    prefix='/answers',
    tags=['Answers']
)

field_names = (
    'id',
    'result'
)

validator = CSVValidator(field_names)

validator.add_header_check('EX1', 'bad header')
validator.add_record_length_check('EX2', 'unexpected record lenght')
validator.add_record_check(check_csv_records)


@router.post('/{task_id}')
async def create_answer(
        file: UploadFile,
        task_id: int,
        db: Session = Depends(get_db),
        user_id: int = Depends(get_current_user_id_or_403),
):
    try:
        csv_reader = csv.reader(StringIO(file.file.read().decode()), delimiter=',')
        csv_data = list(csv_reader)
        problems = validator.validate(csv_reader)

        if problems:
            raise Exception

    except Exception:
        raise HTTPException(detail='CSV is not correct', status_code=400)

    task_ans = {}

    for row in csv_data[1:]:
        id, result = row
        task_ans[id] = result

    answer = create_answer_in_db(
        db=db,
        task_id=task_id,
        user_id=user_id,
        task_ans=task_ans
    )

    # TODO: create background task for calculating score

    return JSONResponse(
        content={
            'answer_id': answer.id
        },
        status_code=201
    )


@router.get('/{task_id}/all')
async def get_all_answers_for_task(
        task_id: int,
        db: Session = Depends(get_db),
        _: int = Depends(get_current_user_id_or_403)
):
    answers = get_all_answers_for_task_in_db(db=db, task_id=task_id)
    result = []

    for answer in answers:
        score, user_id = answer
        result.append({
            'user_id': user_id,
            'score': score
        })

    return JSONResponse(content=result, status_code=200)


@router.get('/{task_id}')
async def get_user_answers_for_task(
        task_id: int,
        db: Session = Depends(get_db),
        user_id: int = Depends(get_current_user_id_or_403)
):
    answers = get_user_answers_for_task_in_db(db=db, task_id=task_id, user_id=user_id)
    return answers
