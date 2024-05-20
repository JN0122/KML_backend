import datetime

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from database.database import get_db
from delivery import crud, dto
from delivery.dto import DeliveryCreate


router = APIRouter(
    prefix="/db",
    tags=["db"],
    responses={404: {"description": "Not found"}},
)


@router.get("/seed")
def seed_database(db: Session = Depends(get_db)):
    if not check_is_empty(db):
        return "Db is not empty"

    with open("data/stacja1_logis.csv", "r") as file:
        for line in file:
            line = line.split(";")

            new_delivery = DeliveryCreate(
                date=datetime.datetime.now().date(),
                time=datetime.datetime.now().time(),
                ulg95=int(line[0]),
                dk=int(line[1]),
                ultsu=int(line[2]),
                ultdk=int(line[3])
            )

            crud.create_delivery(db=db, delivery=new_delivery)

    return "Ok! Db seeded"


def check_is_empty(db: Session = Depends(get_db)):
    all_deliveries = crud.read_deliveries(db=db)
    return all_deliveries == []
