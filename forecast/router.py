from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from database.database import get_db
from delivery import crud as crud_delivery
from forecast import crud as crud_forecast
from forecast import dto as dto_forecast

from forecast.holt_winters.RunModels import RunModels
from forecast.tank_allocation.tank_allocation import process_tank_data


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
def get_forecasts_with_tank_allocation(station_id: int, forecast_len: int, db: Session = Depends(get_db)):
    delivery_models = crud_delivery.read_latest_deliveries_for_station(station_id=station_id, limit=350, db=db)

    run_holt_winters = RunModels(delivery_models)
    forecasts = run_holt_winters.for_every_fuel(forecast_len)

    last_tank_residual = crud_forecast.read_latest_tank_residual_for_station(db, station_id, limit=1)[0]

    json, residual_fuel = process_tank_data(forecasts, last_tank_residual)

    return json
