from datetime import date, timedelta

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

def fill_delivery_gap_with_empty_deliveries(db: Session, start_delivery: dto.DeliveryCreate, end_delivery: dto.DeliveryCreate):
        day_delta = end_delivery.date - start_delivery.date

        if day_delta.days == 1: return
        empty_delivery = dto.DeliveryCreate(
                                station_id=start_delivery.station_id,
                                date=start_delivery.date,
                                time=start_delivery.time,
                                ulg95=0, 
                                dk=0, 
                                ultsu=0, 
                                ultdk=0
                                )
        
        for i in range(1, day_delta.days):
            empty_delivery.date = start_delivery.date + timedelta(i) 
            create_delivery(db, empty_delivery)

def read_all_deliveries(db: Session):
    return db.query(model.Delivery).all()


def read_deliveries_filter(
    db: Session,
    station_id: int | None = None,
    delivery_id: int | None = None,
    delivery_date: date | None = None,
):

    db_deliveries = db.query(model.Delivery)
    if station_id:
        db_deliveries = db_deliveries.filter(model.Delivery.station_id == station_id)
    if delivery_id:
        db_deliveries = db_deliveries.filter(model.Delivery.id == delivery_id)
    if delivery_date:
        db_deliveries = db_deliveries.filter(model.Delivery.date == delivery_date)

    return db_deliveries


def read_latest_deliveries_for_station(db: Session, station_id: int, limit: int = 100):
    db_deliveries = db.query(model.Delivery)

    db_deliveries = (
        db_deliveries.filter(model.Delivery.station_id == station_id)
        .order_by(model.Delivery.date.desc())
        .limit(limit)
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
