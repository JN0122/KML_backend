from sqlalchemy.orm import Session

from delivery import dto
from delivery import model


def create_delivery(db: Session, delivery: dto.DeliveryCreate):
    db_delivery = model.Delivery(
        station_id=delivery.station_id,
        date=delivery.date,
        time=delivery.time,
        ulg95=delivery.ulg95,
        dk=delivery.dk,
        ultsu=delivery.ultsu,
        ultdk=delivery.ultdk,
        total=delivery.get_total(),
    )
    db.add(db_delivery)
    db.commit()
    db.refresh(db_delivery)
    return db_delivery


def read_all_deliveries(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.Delivery).offset(skip).limit(limit).all()


def read_deliveries_by_station_id(db: Session, station_id: int):
    db_deliveries = (
        db.query(model.Delivery).filter(model.Delivery.station_id == station_id)
    )
    return db_deliveries


def update_delivery(db: Session, delivery: dto.DeliveryCreate, delivery_id: int):
    db_delivery = (
        db.query(model.Delivery).filter(model.Delivery.id == delivery_id).first()
    )

    db_delivery.station_id = delivery.station_id
    db_delivery.date = delivery.date
    db_delivery.time = delivery.time
    db_delivery.ulg95 = delivery.ulg95
    db_delivery.dk = delivery.dk
    db_delivery.ultsu = delivery.ultsu
    db_delivery.ultdk = delivery.ultdk
    db_delivery.total = delivery.get_total()

    db.commit()

    updated_db_delivery = (
        db.query(model.Delivery).filter(model.Delivery.id == delivery_id).first()
    )
    return updated_db_delivery


def delete_delivery(db: Session, delivery_id: int):
    db_delivery = (
        db.query(model.Delivery).filter(model.Delivery.id == delivery_id).first()
    )
    db.delete(db_delivery)
    db.commit()
