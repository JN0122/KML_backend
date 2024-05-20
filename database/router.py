import csv
import os

from datetime import datetime

from fastapi import APIRouter
from delivery.dto import DeliveryCreate

from database.seed_database import *


router = APIRouter(
    prefix="/db",
    tags=["db"],
    responses={404: {"description": "Not found"}},
)


@router.get("/seed")
def seed_database(db: Session = Depends(get_db)):
    data_path = "data/"

    if not check_is_empty(db):
        return "Db is not empty"

    station_id = 1
    for station_file in os.listdir(data_path):
        seed_db_from_csv(os.path.join(data_path, station_file), station_id, db)

        station_id += 1

    return "Ok! Db seeded"
