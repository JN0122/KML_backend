from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from database.database import get_db
from delivery import crud, dto

router = APIRouter(
    prefix="/deliveries",
    tags=["deliveries"],
    responses={404: {"description": "Delivery not found"}},
)


@router.post("/", response_model=dto.Delivery)
def create_delivery(delivery: dto.DeliveryCreate, db: Session = Depends(get_db)):
    return crud.create_delivery(db, delivery)


@router.get("/", response_model=list[dto.Delivery])
def read_all_deliveries(db: Session = Depends(get_db)):
    deliveries = crud.read_deliveries(db)
    return deliveries


@router.put("/{delivery_id}", response_model=dto.Delivery)
def update_item(delivery_id: int, delivery: dto.DeliveryCreate, db: Session = Depends(get_db)):
    updated_delivery = crud.update_delivery(db=db, delivery_id=delivery_id, delivery=delivery)
    return updated_delivery


@router.delete("/{delivery_id}")
def delete_delivery(delivery_id: int, db: Session = Depends(get_db)):
    crud.delete_delivery(db, delivery_id)
    return "Delivery deleted"
