from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.app.dependencies import get_db
from app.app.utils import get_superadmin_or_404
from app.app.schemas import Function
from app.app.crud import get_all_functions

router = APIRouter(
    prefix='/functions',
    tags=['Functions']
)


@router.get('/', response_model=Function)
async def get_functions(db: Session = Depends(get_db), _: bool = Depends(get_superadmin_or_404)):
    return get_all_functions(db=db)
