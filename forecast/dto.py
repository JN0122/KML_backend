from datetime import date, time

from pydantic import BaseModel


class ForecastBase(BaseModel):
    date: date
    time: time
    ulg95: int
    dk: int
    ultsu: int
    ultdk: int


class ForecastCreate(ForecastBase):
    pass


class Forecast(ForecastCreate):
    id: int
    total: int

    class Config:
        orm_mode = True
