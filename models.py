
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, Float, String, Sequence
from database import Base

class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, Sequence('address_id_seq'), primary_key=True, index=True)
    name = Column(String, index=True)
    latitude = Column(Float)
    longitude = Column(Float)

    def __init__(self, name, latitude, longitude):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

