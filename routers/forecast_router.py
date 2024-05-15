from fastapi import APIRouter
from datetime import date as d
from forecast import dto, winters_module
from routers.delivery_router import read_all_deliveries

router = APIRouter(
    prefix="/forecast",
    tags=["forecast"],
    responses={404: {"description": "Not found"}},
)


@router.get("/read_all", response_model=list[dto.Forecast])
def read_all_forecasts():
    data = read_all_deliveries()

    model = winters_module.Winters(data)
    coefs = [model.alpha, model.beta, model.gamma, model.season]

    forecast = model.forecast.get(coefs)

    return forecast
