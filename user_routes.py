from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.auth import create_access_token, verify_token
from app.database import get_db
from app.models.user_model import User
from app.schemas.user_schema import (
    UserCreate,
    UserResponse,
    LoginSchema,
    UpdateProfileSchema
)

router = APIRouter()

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


# GET CURRENT USER
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = verify_token(token)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    user = db.query(User).filter(
        User.email == payload["sub"]
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


# SIGNUP
@router.post("/signup")
def signup(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    existing = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    new_user = User(
        name=user.name,
        email=user.email,
        password=pwd_context.hash(user.password),
        role=user.role,
        age=user.age,
        phone=user.phone,
        blood_group=user.blood_group,
        weight=user.weight,
        status="active"
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return {
        "message": "Signup successful"
    }


# LOGIN
@router.post("/login")
def login(
    user: LoginSchema,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not pwd_context.verify(
        user.password,
        existing_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={
            "sub": existing_user.email,
            "role": existing_user.role
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": existing_user.role
    }


# CURRENT USER
@router.get("/users/me", response_model=UserResponse)
def get_me(
    current_user: User = Depends(get_current_user)
):
    return current_user


# UPDATE PROFILE
@router.put("/users/update-profile")
def update_profile(
    data: UpdateProfileSchema,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    if data.fullName:
        current_user.name = data.fullName

    if data.email:
        current_user.email = data.email

    if data.phone:
        current_user.phone = data.phone

    if data.bloodGroup:
        current_user.blood_group = data.bloodGroup

    if data.age:
        current_user.age = data.age

    if data.weight:
        current_user.weight = data.weight

    db.commit()

    db.refresh(current_user)

    return {
        "message": "Profile updated successfully"
    }


# UPDATE AVAILABILITY
@router.post("/users/update-availability")
def update_availability(
    data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    current_user.available = data["is_available"]

    db.commit()

    return {
        "message": "Availability updated",
        "available": current_user.available
    }