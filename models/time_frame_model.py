from sqlalchemy import Column, Integer, String

from database import Base
from enums import Weekday
from datetime import Date, Time


class Delivery(Base):
    __tablename__ = "deliveries"

    id = Column(Integer, primary_key=True, index=True)

    date = Column(Date)
    day = Column(Weekday)
    time = Column(Time)
    ulg95 = Column(Integer)
    dk = Column(Integer)
    ultsu = Column(Integer)
    ultdk =Column(Integer)
    total = Column(Integer)
