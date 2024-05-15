from pydantic import BaseModel
from datetime import date, time


class DeliveryBase(BaseModel):
    date: date
    time: time
    ulg95: int 
    dk: int 
    ultsu: int 
    ultdk: int
    total: int

class DeliveryCreate(DeliveryBase):
    pass

class Delivery(DeliveryCreate):
    id: int

    class Config:
        orm_mode = True