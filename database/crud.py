import os

import csv
from datetime import datetime

from fastapi import Depends
from sqlalchemy.orm import Session
from database.database import get_db

from delivery import crud as crud_delivery
from delivery.dto import DeliveryCreate
from delivery import model as model_delivery

from forecast import crud as crud_forecast
from forecast import dto as dto_forecast
from forecast import model as model_tank_residual

from truck import crud as crud_truck
from truck import dto as dto_truck
from truck import model as model_truck

from station import crud as crud_station
from station import dto as dto_station
from station import model as model_station

from datetime import datetime, timedelta



def seed_database(db: Session = Depends(get_db)):
    data_path = "data/"

    if not __check_is_empty(db):
        return "Db is not empty"

    station_id = 1
    for station_file in os.listdir(data_path):
        __seed_db_from_csv(os.path.join(data_path, station_file), station_id, db)
        __create_empty_tank_residual_for_station(db, station_id)
        __create_stations(db, station_id)
        __create_truck_for_station(db, station_id)
        station_id += 1

    return "Ok! Db seeded"


def delete_database(db: Session = Depends(get_db)):
    db.query(model_delivery.Delivery).delete()
    db.query(model_tank_residual.TankResidual).delete()
    db.commit()

    return "Ok! Db removed"


def reset_database(db: Session = Depends(get_db)):
    delete_database(db=db)
    seed_database(db=db)

    return "Ok! Db was reset"


def __check_is_empty(db: Session = Depends(get_db)):
    all_deliveries = crud_delivery.read_all_deliveries(db=db)
    return all_deliveries == []


def __seed_db_from_csv(path, station_id, db):
    with open(path, newline="") as file:
        has_header = csv.Sniffer().has_header(file.read(1024))

        file_reader = csv.reader(file, delimiter=";", quotechar="|")

        if has_header:
            next(file_reader)

        yesterday = datetime.now().date() - timedelta(days=1)
        for row in file_reader:
            delivery_date = datetime.strptime(row[0], "%d.%m.%Y")
            if delivery_date.date() > yesterday:
                continue
            crud_delivery.create_delivery(
                db=db, delivery=__create_new_delivery(station_id, row)
            )

        return file_reader


def __create_new_delivery(station_id, row):
    new_delivery = DeliveryCreate(
        station_id=station_id,
        date=datetime.strptime(row[0], "%d.%m.%Y"),
        time=datetime.strptime(row[1], "%H:%M").time(),
        ulg95=int(row[2]),
        dk=int(row[3]),
        ultsu=int(row[4]),
        ultdk=int(row[5]),
    )

    return new_delivery


def __create_empty_tank_residual_for_station(db, i):
    lastest_delivery = crud_delivery.read_latest_deliveries_for_station(db, i, 1)
    tank_residual = dto_forecast.TankResidualCreate(
        station_id=i,
        delivery_date=lastest_delivery[0].date,
        ulg95=0,
        dk=0,
        ultsu=0,
        ultdk=0,
    )
    crud_forecast.create_tank_residual(db, tank_residual)


def __create_stations(db: Session, station_id: int):
    ## TODO distance is hardcoded
    new_station = dto_station.StationCreate(name=f"Stacja {station_id}", distance_from_base=station_id*100) 
    crud_station.create_station(db=db, station=new_station)
    

def __create_truck_for_station(db: Session, station_id: int):
    # TODO truck parameters are hardcoded
    if station_id == 1: 
        inspection_date = "2025-03-12"
        brake_pads = 50000
        oil_change = 30000
    else: 
        inspection_date = "2024-12-15"
        brake_pads = 70000
        oil_change = 20000
    new_truck = dto_truck.TruckCreate(station_id=station_id, brake_pads_km_left=brake_pads, oil_change_km_left=oil_change, next_technical_inspection=inspection_date)
    crud_truck.create_truck(db, new_truck)