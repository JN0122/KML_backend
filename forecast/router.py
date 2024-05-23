from fastapi import APIRouter
from forecast.winters.RunWinters import RunWinters
from delivery import crud
from fastapi import Depends
from sqlalchemy.orm import Session
from database.database import get_db

router = APIRouter(
    prefix="/forecasts",
    tags=["forecasts"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
def calculate_forecasts_for_every_fuel(station_id: int, db: Session = Depends(get_db)):
    data = crud.read_deliveries_filter(station_id=station_id, delivery_id=None, delivery_date=None, db=db)
    run_winters = RunWinters()
    return run_winters.for_every_fuel(data)
