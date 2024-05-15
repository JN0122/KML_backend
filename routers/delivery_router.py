from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db
from delivery import crud, dto

router = APIRouter(
    prefix="/delivery",
    tags=["delivery"],
    responses={404: {"description": "Delivery not found"}},
)


@router.get("/read_all", response_model=list[dto.Delivery])
def read_all_deliveries(db: Session = Depends(get_db)):
    deliveries = crud.read_deliveries(db)
    return deliveries


@router.post("/create", response_model=dto.Delivery)
def create_delivery(delivery: dto.DeliveryCreate, db: Session = Depends(get_db)):
    return crud.create_delivery(db=db, delivery=delivery)
