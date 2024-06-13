from fastapi import APIRouter

from fastapi import Depends
from sqlalchemy.orm import Session
from database.database import get_db

from database.crud import seed_database as seed_database_crud 
from database.crud import delete_database as delete_database_crud 
from database.crud import reset_database as reset_database_crud 

router = APIRouter(
    prefix="/db",
    tags=["db"],
    responses={404: {"description": "Not found"}},
)


@router.post("/seed")
def seed_database(db: Session = Depends(get_db)):
    return seed_database_crud(db=db)


@router.delete("/delete")
def delete_database(db: Session = Depends(get_db)):
    return delete_database_crud(db=db)

@router.put("/reset")
def reset_database(db: Session = Depends(get_db)):
    return reset_database_crud(db=db)

