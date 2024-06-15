from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from truck import crud, dto

router = APIRouter(
    prefix="/trucks",
    tags=["trucks"],
    responses={404: {"description": "Truck not found"}},
)

@router.post("/", response_model=dto.Truck)
def create_truck(truck: dto.TruckCreate, db: Session = Depends(get_db)):
    return crud.create_truck(db=db, truck=truck)

@router.get("/", response_model=list[dto.Truck])
def read_trucks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    trucks = crud.get_trucks(db, skip=skip, limit=limit)
    return trucks

@router.get("/{truck_id}", response_model=dto.Truck)
def read_truck(truck_id: int, db: Session = Depends(get_db)):
    db_truck = crud.get_truck(db, truck_id=truck_id)
    if db_truck is None:
        raise HTTPException(status_code=404, detail="Truck not found")
    return db_truck

@router.put("/{truck_id}", response_model=dto.Truck)
def update_truck(truck_id: int, truck: dto.TruckCreate, db: Session = Depends(get_db)):
    db_truck = crud.update_truck(db=db, truck_id=truck_id, truck_update=truck)
    if db_truck is None:
        raise HTTPException(status_code=404, detail="Truck not found")
    return db_truck

@router.delete("/{truck_id}")
def delete_truck(truck_id: int, db: Session = Depends(get_db)):
    db_truck = crud.delete_truck(db, truck_id=truck_id)
    if db_truck is None:
        raise HTTPException(status_code=404, detail="Truck not found")
    return {"message": "Truck deleted"}