from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from station import crud, dto

router = APIRouter(
    prefix="/stations",
    tags=["stations"],
    responses={404: {"description": "Station not found"}},
)

@router.post("/", response_model=dto.Station)
def create_station(station: dto.StationCreate, db: Session = Depends(get_db)):
    db_station = crud.get_station_by_name(db, name=station.name)
    if db_station:
        raise HTTPException(status_code=400, detail="Station already exists")
    return crud.create_station(db=db, station=station)

@router.get("/", response_model=list[dto.Station])
def read_stations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    stations = crud.get_stations(db, skip=skip, limit=limit)
    return stations

@router.get("/{station_id}", response_model=dto.Station)
def read_station(station_id: int, db: Session = Depends(get_db)):
    db_station = crud.get_station(db, station_id=station_id)
    if db_station is None:
        raise HTTPException(status_code=404, detail="Station not found")
    return db_station

@router.put("/{station_id}", response_model=dto.Station)
def update_station(station_id: int, station: dto.StationCreate, db: Session = Depends(get_db)):
    db_station = crud.update_station(db=db, station_id=station_id, station_update=station)
    if db_station is None:
        raise HTTPException(status_code=404, detail="Station not found")
    return db_station

@router.delete("/{station_id}")
def delete_station(station_id: int, db: Session = Depends(get_db)):
    db_station = crud.delete_station(db, station_id=station_id)
    if db_station is None:
        raise HTTPException(status_code=404, detail="Station not found")
    return {"message": "Station deleted"}