from pydantic import BaseModel
from datetime import date

class TruckBase(BaseModel):
    station_id: int
    brake_pads_km: int
    oil_change_km: int
    next_technical_inspection: date
    last_oil_change: date
    last_brake_pads_change: date

class TruckCreate(TruckBase):
    pass

class Truck(TruckBase):
    id: int

    class Config:
        orm_mode = True