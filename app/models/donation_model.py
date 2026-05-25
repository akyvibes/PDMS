from sqlalchemy import Column, Integer, String
from app.database import Base

class Donation(Base):
    __tablename__ = "donations"

    id = Column(Integer, primary_key=True, index=True)

    donor_email = Column(String(100))

    date = Column(String(50))

    center = Column(String(100))

    type = Column(String(50))

    status = Column(String(50))