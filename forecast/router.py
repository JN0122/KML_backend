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
def calculate_future_forecasts(station_id: int, db: Session = Depends(get_db)):
    data = crud.read_deliveries_filter(station_id=station_id, db=db)

    return RunWinters.for_every_fuel(data)
