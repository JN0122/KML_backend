from datetime import date, time

from pydantic import BaseModel


class DeliveryBase(BaseModel):
    date: date
    time: time
    ulg95: int
    dk: int
    ultsu: int
    ultdk: int


class DeliveryCreate(DeliveryBase):
    pass


class Delivery(DeliveryCreate):
    id: int
    total: int

    class Config:
        orm_mode = True
