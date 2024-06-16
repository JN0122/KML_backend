from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from truck import crud as crud_truck, dto as dto_truck
from station import crud as crud_station
from delivery import crud as crud_delivery
from utilsalgorithm.calculations import calculate_trips_left

router = APIRouter(
    prefix="/trucks",
    tags=["trucks"],
    responses={404: {"description": "Truck not found"}},
)

@router.get("/", response_model=list[dto_truck.Truck])
def read_trucks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    trucks = crud_truck.get_trucks(db, skip=skip, limit=limit)
    return trucks

@router.get("/{truck_id}", response_model=dto_truck.Truck)
def read_truck(truck_id: int, db: Session = Depends(get_db)):
    db_truck = crud_truck.get_truck(db, truck_id=truck_id)
    return db_truck

@router.put("/{truck_id}", response_model=dto_truck.Truck)
def update_truck(truck_id: int, truck: dto_truck.TruckCreate, db: Session = Depends(get_db)):
    db_truck = crud_truck.update_truck(db=db, truck_id=truck_id, truck_update=truck)
    if db_truck is None:
        raise HTTPException(status_code=404, detail="Truck not found")
    return db_truck

@router.delete("/{truck_id}")
def delete_truck(truck_id: int, db: Session = Depends(get_db)):
    db_truck = crud_truck.delete_truck(db, truck_id=truck_id)
    if db_truck is None:
        raise HTTPException(status_code=404, detail="Truck not found")
    return {"message": "Truck deleted"}

@router.get("/{truck_id}/get_all_details")
def get_all_details_for_truck(truck_id: int, db: Session = Depends(get_db)):
    db_truck = crud_truck.get_truck(db, truck_id)
    station = crud_station.get_station(db, db_truck.station_id)
    last_delivery = crud_delivery.read_latest_deliveries_for_station(db, db_truck.station_id, 1)[0]

    deliveries_since_last_brake_pads_change_count = crud_delivery.get_deliveries_count_from_date_for_station(db, db_truck.station_id, db_truck.last_brake_pads_change)
    deliveries_since_last_oil_change_count = crud_delivery.get_deliveries_count_from_date_for_station(db, db_truck.station_id, db_truck.last_oil_change)

    brake_pads_info = calculate_trips_left(station.distance_from_base, deliveries_since_last_brake_pads_change_count, db_truck.brake_pads_km)
    oil_info = calculate_trips_left(station.distance_from_base, deliveries_since_last_oil_change_count, db_truck.oil_change_km)

    days_left_to_next_inspection = db_truck.next_technical_inspection - last_delivery.date
    response = [{
        "station_id": station.id, 
        "distance_from_base": station.distance_from_base,
        "next_technical_inspection":db_truck.next_technical_inspection,  
        "left_to_next_inspection": days_left_to_next_inspection.days,
        "last_brake_pads_change": db_truck.last_brake_pads_change,
        "brake_pads_trips_left": brake_pads_info[1], 
        "brake_pads_km_left":brake_pads_info[0],
        "last_oil_change":db_truck.last_oil_change,
        "oil_change_trips_left":oil_info[1], 
        "oil_change_km_left":oil_info[0],
    }]
    return response