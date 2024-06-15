from sqlalchemy.orm import Session
from station import dto
from station import model

def create_station(db: Session, station: dto.StationCreate):
    db_station = model.Station(
        name=station.name,
        distance_from_base=station.distance_from_base,
    )
    db.add(db_station)
    db.commit()
    db.refresh(db_station)
    return db_station

def get_station(db: Session, station_id: int):
    return db.query(model.Station).filter(model.Station.id == station_id).first()

def get_station_by_name(db: Session, name: str):
    return db.query(model.Station).filter(model.Station.name == name).first()

def get_stations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.Station).offset(skip).limit(limit).all()

def update_station(db: Session, station_id: int, station_update: dto.StationCreate):
    db_station = get_station(db, station_id)
    if not db_station:
        return None

    db_station.name = station_update.name
    db_station.distance_from_base = station_update.distance_from_base
    db.commit()
    db.refresh(db_station)
    return db_station

def delete_station(db: Session, station_id: int):
    db_station = get_station(db, station_id)
    if not db_station:
        return None
    db.delete(db_station)
    db.commit()
    return db_station