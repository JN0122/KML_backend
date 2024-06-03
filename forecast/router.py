from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from database.database import get_db
from delivery import crud
from forecast.winters.RunModels import RunModels

router = APIRouter(
    prefix="/forecasts",
    tags=["forecasts"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
def calculate_forecasts_for_every_fuel(station_id: int, forecast_len: int, db: Session = Depends(get_db)):
    data = crud.read_deliveries_for_winters(station_id=station_id, limit=350, db=db)

    run_winters = RunModels()
    result = run_winters.holt_winters_for_every_fuel(data, forecast_len)
    return result
