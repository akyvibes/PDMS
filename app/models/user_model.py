from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, default=18)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    phone = Column(String(20), nullable=True)
    blood_group = Column(String(10), nullable=True)
    role = Column(String(20), default="donor")
    is_banned = Column(Boolean, default=False)
    available = Column(Boolean, default=True)
    status = Column(String(50), default="active")
    weight = Column(Integer, default=0)
    profile_image_url = Column(String(255), nullable=True)
