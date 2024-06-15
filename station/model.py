from sqlalchemy import Column, Integer, String, Float
from database.database import Base

class Station(Base):
    __tablename__ = "stations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    distance_from_base = Column(Float, nullable=False)