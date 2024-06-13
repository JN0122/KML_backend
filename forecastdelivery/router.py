from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from database.database import get_db
from delivery import crud
from forecast.router import get_forecasts
from helpers.ModelDtoCasting import ModelDtoCasting

router = APIRouter(
    prefix="/forecasts_and_deliveries",
    tags=["forecasts and deliveries"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
def get_forecasts_and_deliveries(station_id: int, delivery_len: int = 20, forecast_len: int = 10, db: Session = Depends(get_db)):
    delivery_models = crud.read_latest_deliveries_for_station(db, station_id, delivery_len)
    delivery_dtos = ModelDtoCasting.delivery_models_to_delivery_dtos(delivery_models)

    forecasts = get_forecasts(station_id, delivery_len + forecast_len, db)
    start_date = min([delivery.date for delivery in delivery_models])
    ModelDtoCasting.change_forecast_start_date(start_date, forecasts)

    deliveryforecasts = ModelDtoCasting.forecast_and_delivery_model_to_deliveryforecast_dto(forecasts=forecasts, deliveries=delivery_dtos)
    return deliveryforecasts
