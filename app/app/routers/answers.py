import csv
from io import StringIO
from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    UploadFile,
    BackgroundTasks
)
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from csvvalidator import CSVValidator

from app.app.models import Answer
from app.app.dependencies import get_db
from app.app.utils import (
    get_current_user_id_or_403,
    check_csv_records,
    MAE,
    MAPE,
    MSE
)
from app.app.crud import (
    create_answer_in_db,
    get_all_answers_for_task_in_db,
    get_user_answers_for_task_in_db,
    get_task_from_db,
    update_score_in_db
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


def calculate_score(db: Session, answer: Answer, task_id: int) -> None:
    task = get_task_from_db(db=db, task_id=task_id)

    function_name = task.function.name
    correct_answers = [float(answer) for answer in task.task_ans.values()]
    user_answers = [float(answer) for answer in answer.task_ans.values()]

    if function_name == 'MSE':
        function = MSE(y_real=correct_answers, y_predicted=user_answers)
    elif function_name == 'MAPE':
        function = MAPE(y_real=correct_answers, y_predicted=user_answers)
    elif function_name == 'MAE':
        function = MAE(y_real=correct_answers, y_predicted=user_answers)

    score = function.calc()

    update_score_in_db(db=db, answer_id=answer.id, score=score)


@router.post('/{task_id}')
async def create_answer(
        file: UploadFile,
        task_id: int,
        background_tasks: BackgroundTasks,
        db: Session = Depends(get_db),
        user_id: int = Depends(get_current_user_id_or_403),
):
    task = get_task_from_db(db=db, task_id=task_id)

    if not task:
        raise HTTPException(detail='Task not found', status_code=404)

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
        task_ans[id] = result.strip()

    if len(task_ans) != len(task.task_ans):
        raise HTTPException(detail='CSV len is not correct', status_code=400)

    answer = create_answer_in_db(
        db=db,
        task_id=task_id,
        user_id=user_id,
        task_ans=task_ans
    )

    background_tasks.add_task(calculate_score, db=db, answer=answer, task_id=task_id)

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
