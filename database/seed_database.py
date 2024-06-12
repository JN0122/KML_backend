import csv
from datetime import datetime

from fastapi import Depends
from sqlalchemy.orm import Session

from database.database import get_db
from delivery import crud as crud_delivery
from delivery.dto import DeliveryCreate

from forecast import crud as crud_forecast
from forecast import dto as dto_forecast


def check_is_empty(db: Session = Depends(get_db)):
    all_deliveries = crud_delivery.read_all_deliveries(db=db)
    return all_deliveries == []


def seed_db_from_csv(path, station_id, db):
    with open(path, newline="") as file:
        has_header = csv.Sniffer().has_header(file.read(1024))

        file_reader = csv.reader(file, delimiter=';', quotechar='|')

        if has_header:
            next(file_reader)

        for row in file_reader:
            crud_delivery.create_delivery(db=db, delivery=create_new_delivery(station_id, row))

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

def create_empty_tank_residual_for_station(db, i):
    lastest_delivery = crud_delivery.read_latest_deliveries_for_station(db, i, 1)
    tank_residual = dto_forecast.TankResidualCreate(station_id=i, delivery_date=lastest_delivery[0].date, ulg95=0, dk=0, ultsu=0, ultdk=0)
    crud_forecast.create_tank_residual(db, tank_residual)
