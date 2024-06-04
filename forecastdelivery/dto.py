from datetime import date, time 

from pydantic import BaseModel

class ForecastDelivery(BaseModel):
    id: int
    station_id: int
    date: date
    time: time
    ulg95: int
    dk: int
    ultsu: int
    ultdk: int
    ulg95_forecast: float
    dk_forecast: float
    ultsu_forecast: float
    ultdk_forecast: float

