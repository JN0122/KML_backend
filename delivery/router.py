from datetime import date

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from database.database import get_db
from delivery import crud, dto
from forecast import crud as crud_forecast

from forecast.holt_winters.RunModels import RunModels
from forecast.tank_allocation.tank_allocation import allocate_tanks
from forecast.helper import *
from helpers.DataConverters.TankAllocationConverter import TankAllocationConverter

router = APIRouter(
    prefix="/deliveries",
    tags=["deliveries"],
    responses={404: {"description": "Delivery not found"}},
)


@router.post("/", response_model=dto.Delivery)
def create_delivery(delivery: dto.DeliveryCreate, db: Session = Depends(get_db)):
    return crud.create_delivery(db, delivery)


@router.post("/approve", response_model=dto.Delivery)
def approve_delivery(station_id: int, db: Session = Depends(get_db)):
    tank_allocation, residual = get_forecasts_with_tank_allocation_and_residuals(station_id, db)

    previous_delivery = crud.read_latest_deliveries_for_station(db, station_id, limit=1)[0]
    delivery_create = TankAllocationConverter.get_delivery_create_from_tank_allocation(tank_allocation)

    crud.fill_delivery_gap_with_empty_deliveries(db, previous_delivery, delivery_create)
    delivery_created = crud.create_delivery(db, delivery_create)

    crud_forecast.create_tank_residual(tank_residual=residual, db=db)

    return delivery_created


@router.get("/", response_model=list[dto.Delivery])
def read_all_deliveries(db: Session = Depends(get_db)):
    deliveries = crud.read_all_deliveries(db)
    return deliveries


@router.get("/filter", response_model=list[dto.Delivery])
def read_deliveries_filter(
    delivery_id: int | None = None,
    station_id: int | None = None,
    delivery_date: date | None = None,
    db: Session = Depends(get_db),
):
    deliveries = crud.read_deliveries_filter(
        db, delivery_id=delivery_id, station_id=station_id, delivery_date=delivery_date
    )
    return deliveries


@router.get("/latest", response_model=list[dto.Delivery])
def read_latest_deliveries(
    station_id: int | None = None,
    limit: int | None = None,
    db: Session = Depends(get_db),
):
    deliveries = crud.read_latest_deliveries_for_station(
        db=db, station_id=station_id, limit=limit
    )
    return deliveries


@router.put("/{delivery_id}", response_model=dto.Delivery)
def update_delivery(
    delivery_id: int, delivery: dto.DeliveryCreate, db: Session = Depends(get_db)
):
    updated_delivery = crud.update_delivery(
        db=db, delivery_id=delivery_id, delivery=delivery
    )
    return updated_delivery


@router.delete("/{delivery_id}")
def delete_delivery(delivery_id: int, db: Session = Depends(get_db)):
    crud.delete_delivery(db, delivery_id)
    return "Delivery deleted"
