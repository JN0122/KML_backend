from pydantic import BaseModel

class StationBase(BaseModel):
    name: str
    distance_from_base: float

class StationCreate(StationBase):
    pass

class Station(StationBase):
    id: int

    class Config:
        orm_mode = True