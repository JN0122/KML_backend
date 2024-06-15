from pydantic import BaseModel
from datetime import date

class TruckBase(BaseModel):
    station_id: int
    brake_pads_km_left: int
    oil_change_km_left: int
    next_technical_inspection: date

class TruckCreate(TruckBase):
    pass

class Truck(TruckBase):
    id: int

    class Config:
        orm_mode = True