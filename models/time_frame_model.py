from sqlalchemy import create_engine, Column, Integer, String
from pydantic import BaseModel


class TimeFrame(Base):
    __tablename__ = "time_frames"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
