from sqlalchemy.orm import Session

from delivery import dto
from delivery import model


def read_delivery_by_id(db: Session, delivery_id: int):
    return db.query(model.Delivery).filter(model.Delivery == delivery_id).first()


def read_deliveries(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.Delivery).offset(skip).limit(limit).all()


def create_delivery(db: Session, delivery: dto.DeliveryCreate):
    db_delivery = model.Delivery(
        date=delivery.date,
        time=delivery.time,
        ulg95=delivery.ulg95,
        dk=delivery.dk,
        ultsu=delivery.ultsu,
        ultdk=delivery.ultdk,
        total=delivery.ulg95 + delivery.dk + delivery.ultsu + delivery.ultdk,
    )
    db.add(db_delivery)
    db.commit()
    db.refresh(db_delivery)
    return db_delivery
