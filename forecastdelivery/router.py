from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from database.database import get_db
from delivery import crud
from forecast.winters.RunWinters import RunWinters

router = APIRouter(
    prefix="/forecasts_and_deliveries",
    tags=["forecasts and deliveries"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{station_id}")
def get_forecasts_and_deliveries(station_id: int, db: Session = Depends(get_db)):
    data = crud.read_deliveries_for_winters(station_id=station_id, limit=350, db=db)
    run_winters = RunWinters()
    forecasts = run_winters.for_every_fuel(data)
    deliveries = crud.read_all_deliveries(db)
    return deliveries+forecasts