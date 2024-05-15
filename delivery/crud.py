from sqlalchemy.orm import Session

from delivery import model 
from delivery import dto


def get_delivery_by_id(db: Session, delivery_id: int):
    return db.query(model.Delivery).filter(model.Delivery == delivery_id).first()


def get_deliveries(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.Delivery).offset(skip).limit(limit).all()
