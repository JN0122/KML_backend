from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base

class Truck(Base):
    __tablename__ = "trucks"

    id = Column(Integer, primary_key=True, index=True)
    station_id = Column(Integer, ForeignKey("stations.id"), nullable=False)
    brake_pads_km_left = Column(Integer, nullable=False)
    oil_change_km_left = Column(Integer, nullable=False)
    next_technical_inspection = Column(Date, nullable=False)
    
    station = relationship("Station", back_populates="trucks")
