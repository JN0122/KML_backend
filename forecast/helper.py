from fastapi import Depends
from sqlalchemy.orm import Session

from database.database import get_db
from delivery import crud as crud_delivery
from forecast import crud as crud_forecast

from forecast.holt_winters.RunModels import RunModels
from forecast.tank_allocation.tank_allocation import allocate_tanks


def get_forecasts_with_tank_allocation_and_residuals(station_id: int, db: Session = Depends(get_db)):
    delivery_models = crud_delivery.read_latest_deliveries_for_station(station_id=station_id, limit=350, db=db)

    run_holt_winters = RunModels(delivery_models)
    forecasts = run_holt_winters.for_every_fuel(30)

    last_tank_residual = crud_forecast.read_latest_tank_residual_for_station(db, station_id)

    return allocate_tanks(forecasts, last_tank_residual)
