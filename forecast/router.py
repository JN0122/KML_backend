from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from database.database import get_db
from delivery import crud

from forecast.winters.RunModels import RunModels
from forecast.tank_allocation import process_tank_data

router = APIRouter(
    prefix="/forecasts",
    tags=["forecasts"],
    responses={404: {"description": "Not found"}},
)



@router.get("/")
def get_forecasts(station_id: int, forecast_len: int, db: Session = Depends(get_db)):
    data = crud.read_latest_deliveries_for_station(station_id=station_id, limit=350, db=db)

    run_winters = RunModels()
    result = run_winters.holt_winters_for_every_fuel(data, forecast_len)
    return result

@router.get("/{station_id}")
def calculate_forecasts_for_every_fuel(station_id: int, db: Session = Depends(get_db)):
    data = crud.read_latest_deliveries_for_station(station_id=station_id, limit=350, db=db)
    run_models = RunModels()
    return run_models.holt_winters_for_every_fuel(data, 100)


@router.get("/tank_allocation/{station_id}")
def calculate_tank_allocation(station_id: int, db: Session = Depends(get_db)):
    data = {
        "ulg95": {
            "1": 1000, "2": 1000, "3": 1000, "4": 1000, "5": 1000,
            "6": 1000, "7": 1000, "8": 1000, "9": 1000, "10": 1000
        },
        "dk": {
            "1": 1000, "2": 1000, "3": 1000, "4": 1000, "5": 1000,
            "6": 1000, "7": 1000, "8": 1000, "9": 1000, "10": 1000
        },
        "ultsu": {
            "1": 1000, "2": 1000, "3": 1000, "4": 1000, "5": 1000,
            "6": 1000, "7": 1000, "8": 1000, "9": 1000, "10": 1000
        },
        "ultdk": {
            "1": 1000, "2": 1000, "3": 1000, "4": 1000, "5": 1000,
            "6": 1000, "7": 1000, "8": 1000, "9": 1000, "10": 1000
        }
    }
    start_date_str = "2024-01-01"
    return process_tank_data(data, start_date_str, station_id)

