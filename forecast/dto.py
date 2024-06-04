from datetime import date

from pydantic import BaseModel

class Forecast(BaseModel):
    station_id: int
    date: date
    ulg95_forecast: float
    dk_forecast: float
    ultsu_forecast: float
    ultdk_forecast: float
    id: int
