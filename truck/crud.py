from sqlalchemy.orm import Session
from truck import dto, model

def create_truck(db: Session, truck: dto.TruckCreate):
    db_truck = model.Truck(
        station_id=truck.station_id,
        brake_pads_km=truck.brake_pads_km,
        oil_change_km=truck.oil_change_km,
        next_technical_inspection=truck.next_technical_inspection,
        last_oil_change=truck.last_oil_change,
        last_brake_pads_change=truck.last_brake_pads_change
    )
    db.add(db_truck)
    db.commit()
    db.refresh(db_truck)
    return db_truck

def get_truck(db: Session, truck_id: int):
    return db.query(model.Truck).filter(model.Truck.id == truck_id).first()

def get_trucks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.Truck).offset(skip).limit(limit).all()

def update_truck(db: Session, truck_id: int, truck_update: dto.TruckCreate):
    db_truck = get_truck(db, truck_id)
    if not db_truck:
        return None

    db_truck.station_id = truck_update.station_id
    db_truck.brake_pads_km = truck_update.brake_pads_km
    db_truck.oil_change_km = truck_update.oil_change_km
    db_truck.next_technical_inspection = truck_update.next_technical_inspection
    db.commit()
    db.refresh(db_truck)
    return db_truck

def delete_truck(db: Session, truck_id: int):
    db_truck = get_truck(db, truck_id)
    if not db_truck:
        return None
    db.delete(db_truck)
    db.commit()
    return db_truck