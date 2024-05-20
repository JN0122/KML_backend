from fastapi import Depends
from sqlalchemy.orm import Session
from delivery import crud, dto
from database.database import get_db
from datetime import datetime
from delivery.dto import DeliveryCreate
import csv


def check_is_empty(db: Session = Depends(get_db)):
    all_deliveries = crud.read_all_deliveries(db=db)
    return all_deliveries == []


def seed_db_from_csv(path, station_id, db):
    with open(path, newline="") as file:
        has_header = csv.Sniffer().has_header(file.read(1024))

        file_reader = csv.reader(file, delimiter=';', quotechar='|')

        if has_header:
            next(file_reader)

        for row in file_reader:
            crud.create_delivery(db=db, delivery=create_new_delivery(station_id, row))

        return file_reader


def create_new_delivery(station_id, row):
    new_delivery = DeliveryCreate(
        station_id=station_id,
        date=datetime.strptime(row[0], '%d.%m.%Y'),
        time=datetime.strptime(row[1], '%H:%M').time(),
        ulg95=int(row[2]),
        dk=int(row[3]),
        ultsu=int(row[4]),
        ultdk=int(row[5])
    )

    return new_delivery
