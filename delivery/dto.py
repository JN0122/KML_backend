from datetime import date, time

from pydantic import BaseModel


class DeliveryBase(BaseModel):
    station_id: int
    date: date
    time: time
    ulg95: int
    dk: int
    ultsu: int
    ultdk: int

    def get_total(self) -> int:
        return self.ulg95 + self.dk + self.ultsu + self.ultdk

    def get_delivery_for_every_fuel(self) -> dict:
        return {
            "ulg95": self.ulg95,
            "dk": self.dk,
            "ultsu": self.ultsu,
            "ultdk": self.ultdk
        }

class DeliveryCreate(DeliveryBase):
    pass


class Delivery(DeliveryCreate):
    id: int
    total: int

    class Config:
        orm_mode = True
