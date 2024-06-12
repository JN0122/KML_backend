from sqlalchemy.orm import Session

from forecast import dto
from forecast import model


def create_tank_residual(db: Session, tank_residual: dto.TankResidualCreate):
    db_tank_residual = model.TankResidual(
        station_id=tank_residual.station_id,
        delivery_date=tank_residual.delivery_date,
        ulg95=tank_residual.ulg95,
        dk=tank_residual.dk,
        ultsu=tank_residual.ultsu,
        ultdk=tank_residual.ultdk,
    )
    db.add(db_tank_residual)
    db.commit()
    db.refresh(db_tank_residual)
    return db_tank_residual

def read_latest_tank_residual_for_station(db: Session, station_id: int):
    db_tank_residuals = db.query(model.TankResidual)

    db_tank_residuals = (db_tank_residuals
                     .filter(model.TankResidual.station_id == station_id)
                     .order_by(model.TankResidual.delivery_date.desc())
                     .limit(1))

    return db_tank_residuals[0]
