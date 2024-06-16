from datetime import date

from pydantic import BaseModel
from forecast.model import TankResidual

class Forecast(BaseModel):
    station_id: int
    date: date
    ulg95_forecast: float
    dk_forecast: float
    ultsu_forecast: float
    ultdk_forecast: float

class DeliveryForecast(Forecast):
    ulg95: int | None
    dk: int | None
    ultsu: int | None
    ultdk: int | None
    id: int

class TankResidualBase(BaseModel):
    station_id: int
    delivery_date: date
    ulg95: float
    dk: float
    ultsu: float
    ultdk: float

    def add_fuel(self, type: str, liters: float):
        if type == "ulg95":
            self.ulg95 = liters
        elif type == "dk":
            self.dk = liters
        elif type == "ultsu":
            self.ultsu = liters
        elif type == "ultdk":
            self.ultdk = liters

    def add_fuel_from_list(self, residual: list[tuple]):
        for fuel in residual:
            self.add_fuel(fuel[0], fuel[1])
    
    def is_empty(self) -> bool:
        if self.ulg95 or self.dk or self.ultsu or self.ultdk:
            return False
        return True


class TankPartition(TankResidualBase):
    tank_id: int
    capacity: int


class TankResidualCreate(TankResidualBase):
    def add_fuel_from_partitions(self, tank_partitions: list[TankPartition]):
        for partition in tank_partitions:
            self.ulg95 += partition.ulg95
            self.dk += partition.dk
            self.ultsu += partition.ultsu
            self.ultdk += partition.ultdk

    @staticmethod
    def convert_model(model: TankResidual):
        return TankResidualCreate(
            station_id=model.station_id,
            delivery_date=model.delivery_date,
            ulg95=model.ulg95,
            dk=model.dk,
            ultsu=model.ultsu,
            ultdk=model.ultdk
        )
