from pydantic import BaseModel, EmailStr
from typing import Optional

#   User Schemas
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str 
    role: str
    age: int | None = None
    phone: str | None = None
    blood_group: str | None = None
    weight: int | None = None
    profile_image_url: str | None = None
    status: str | None = None

#   User Response Schema
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    age: int | None = None
    phone: str | None = None
    blood_group: str | None = None
    available: bool
    is_banned: bool
    status: str
    weight: int | None = None
    profile_image_url: str | None = None

    class Config:
        from_attributes = True

#   Login Schema
class LoginSchema(BaseModel):
    email: EmailStr
    password: str

#   User Update Schema
class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    role: str | None = None
    phone: str | None = None
    blood_group: str | None = None
    age: int | None = None
    weight: int | None = None
    profile_image_url: str | None = None
    status: str | None = None
    password: str | None = None

#   Update Profile Schema
class UpdateProfileSchema(BaseModel):
    fullName: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    bloodGroup: str | None = None
    age: int | None = None
    weight: int | None = None
    profile_image_url: str | None = None