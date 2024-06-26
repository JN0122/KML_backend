from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from database.database import get_db
from delivery import crud as crud_delivery

from forecast.holt_winters.RunModels import RunModels
from forecast.helper import *


router = APIRouter(
    prefix="/forecasts",
    tags=["forecasts"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
def get_forecasts(station_id: int, forecast_len: int, db: Session = Depends(get_db)):
    delivery_models = crud_delivery.read_latest_deliveries_for_station(station_id=station_id, limit=350, db=db)

    run_holt_winters = RunModels(delivery_models)
    return run_holt_winters.for_every_fuel_as_dtos(forecast_len)


@router.get("/with_tank_allocation")
def get_forecasts_with_tank_allocation(station_id: int, db: Session = Depends(get_db)):
    tank_allocation, _ = get_forecasts_with_tank_allocation_and_residuals(station_id, db)
    return tank_allocation
