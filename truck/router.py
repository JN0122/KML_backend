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

@router.post("/", response_model=dto_truck.Truck)
def create_truck(truck: dto_truck.TruckCreate, db: Session = Depends(get_db)):
    return crud_truck.create_truck(db=db, truck=truck)

@router.get("/{truck_id}/trips_left")
def get_trips_left(truck_id: int, db: Session = Depends(get_db)):
    
    db_truck = crud_truck.get_truck(db, truck_id)
    if db_truck is None:
        raise HTTPException(status_code=404, detail="Truck not found")

    station = crud_station.get_station(db, db_truck.station_id) 
    if station is None:
        raise HTTPException(status_code=404, detail="Station for truck not found")

    trips_left = calculate_trips_left(
        distance=station.distance_from_base,
        brake_pads_km_left=db_truck.brake_pads_km_left,
        oil_change_km_left=db_truck.oil_change_km_left
    )
    return trips_left

@router.get("/", response_model=list[dto_truck.Truck])
def read_trucks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    trucks = crud_truck.get_trucks(db, skip=skip, limit=limit)
    return trucks

@router.get("/{truck_id}", response_model=dto_truck.Truck)
def read_truck(truck_id: int, db: Session = Depends(get_db)):
    db_truck = crud_truck.get_truck(db, truck_id=truck_id)
    if db_truck is None:
        raise HTTPException(status_code=404, detail="Truck not found")
    return db_truck

@router.get("/{truck_id}/brake_pads", response_model=dict)
def get_brake_pads_info(truck_id: int, db: Session = Depends(get_db)):
    db_truck = crud_truck.get_truck(db, truck_id)
    if db_truck is None:
        raise HTTPException(status_code=404, detail="Truck not found")

    return {"brake_pads_km_left": db_truck.brake_pads_km_left}

@router.get("/{truck_id}/oil", response_model=dict)
def get_oil_info(truck_id: int, db: Session = Depends(get_db)):
    db_truck = crud_truck.get_truck(db, truck_id)
    if db_truck is None:
        raise HTTPException(status_code=404, detail="Truck not found")

    return {"oil_change_km_left": db_truck.oil_change_km_left}


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

    break_pads = get_brake_pads_info(truck_id, db)
    oil = get_oil_info(truck_id, db)
    trips_left = get_trips_left(truck_id, db)

    days_left_to_next_inspection = db_truck.next_technical_inspection - last_delivery.date

    response = {
        "station_id": station.id, 
        "distance_from_base": station.distance_from_base, 
        "next_technical_inspection":db_truck.next_technical_inspection,  
        "left_to_next_inspection": days_left_to_next_inspection.days,
        **break_pads, 
        **oil, 
        **trips_left
    }
    return response