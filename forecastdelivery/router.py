from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from database.database import get_db
from delivery import crud
from forecast.router import get_forecasts
from forecast.winters.DataConverter import DataConverter

router = APIRouter(
    prefix="/forecasts_and_deliveries",
    tags=["forecasts and deliveries"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
def get_forecasts_and_deliveries(station_id: int, forecast_len: int, db: Session = Depends(get_db)):
    delivery_models = crud.read_latest_deliveries_for_station(db, station_id, forecast_len)
    deliveries_converted = DataConverter(delivery_models)

    forecasts = get_forecasts(station_id, forecast_len, db)


    return deliveries_converted.deliveries
