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

    def get_total(self):
        return self.ulg95 + self.dk + self.ultsu + self.ultdk


class DeliveryCreate(DeliveryBase):
    pass


class Delivery(DeliveryCreate):
    id: int
    total: int

    class Config:
        orm_mode = True
