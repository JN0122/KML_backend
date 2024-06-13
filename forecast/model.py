from sqlalchemy import Column, Integer, Date, Float

from database.database import Base


class TankResidual(Base):
    __tablename__ = "tank_residual"

    id = Column(Integer, primary_key=True, index=True)

    station_id = Column(Integer)
    delivery_date = Column(Date)
    ulg95 = Column(Float)
    dk = Column(Float)
    ultsu = Column(Float)
    ultdk = Column(Float)
