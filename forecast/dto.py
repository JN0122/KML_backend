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

class TankResidualBase(BaseModel):
    station_id: int
    delivery_date: date
    ulg95: float
    dk: float
    ultsu: float
    ultdk: float

    def add_tank_residual_from_list(self, residual: list[tuple]):
        for fuel in residual:
            if fuel[0] == "ulg95":
                self.ulg95 = fuel[1]
            elif fuel[0] == "dk":
                self.dk = fuel[1]
            elif fuel[0] == "ultsu":
                self.ultsu = fuel[1]
            elif fuel[0] == "ultdk":
                self.ultdk = fuel[1]

class TankResidualCreate(TankResidualBase):
    pass
