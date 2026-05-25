from sqlalchemy import Column, Integer, String
from app.database import Base


class BloodRequest(Base):

    __tablename__ = "blood_requests"

    id = Column(Integer, primary_key=True, index=True)

    patient_name = Column(String(100))

    blood_group = Column(String(10))

    hospital = Column(String(100))

    units = Column(Integer)

    status = Column(String(50), default="pending")