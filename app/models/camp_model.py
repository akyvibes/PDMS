from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Camp(Base):
    __tablename__ = "camps"

    id = Column(Integer, primary_key=True, index=True)

    day = Column(String)

    month = Column(String)

    title = Column(String)

    location = Column(String)

    donors = Column(Integer, default=0)

    time = Column(String)

    type = Column(String)

    status = Column(String)

    latitude = Column(Float)

    longitude = Column(Float)