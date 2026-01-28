from sqlalchemy import( String,Integer,Float,DateTime,Column,Text)

from mysql_connection import engine

from sqlalchemy.orm import declarative_base

base = declarative_base()

class Earthquakes(base):
    __tablename__ = "earthquakes"
    id = Column(String(255), primary_key = True)
    time = Column(DateTime)
    updated = Column(DateTime)
    latitude = Column(Float)
    longitude = Column(Float)
    depth_km  = Column(Float)
    mag = Column(Float)
    magType = Column(String(255))
    place = Column(Text) 
    status  = Column(String(255))
    tsunami = Column(Integer)
    sig = Column(Integer)
    net =  Column(String(255))
    nst =  Column(Integer)
    dmin  = Column(Float)
    rms  = Column(Float)
    gap  = Column(Float)
    magError = Column(Float)
    depthError = Column(Float)
    magNst  = Column(Float)
    locationSource  = Column(String(255))
    magSource  = Column(String(255)) 
    types = Column(Text) 
    ids  = Column(Text) 
    sources = Column(Text) 
    type  = Column(String(255))
    alert = Column(String(255))
    Country = Column(String(255))
    years = Column(Integer)
    month = Column(Integer)
    day = Column(Integer)
    day_of_week = Column(String(255))
    depth_flag  = Column(String(255))
    destructive_flag = Column(String(255))

base.metadata.create_all(engine) 
print("table created successfully")   