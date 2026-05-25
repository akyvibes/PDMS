from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.user_model import User

router = APIRouter(prefix="/admin")

# DATABASE SESSION
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# GET ALL USERS
@router.get("/users")
def get_users(db: Session = Depends(get_db)):

    users = db.query(User).all()

    result = []

    for user in users:
        result.append({
            "id": user.id,
            "name": user.full_name if hasattr(user, "full_name") else user.email,
            "email": user.email,
            "role": user.role,
            "blood": getattr(user, "blood_group", "O+"),
            "status": getattr(user, "status", "Active")
        })

    return result


# CREATE USER
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

@router.post("/users")
def create_user(data: dict, db: Session = Depends(get_db)):

    new_user = User(
        name=data.get("name"),
        email=data.get("email"),
        password=pwd_context.hash("123456"),
        role=data.get("role"),
        blood_group=data.get("blood"),
        status=data.get("status", "active"),
        age=18,
        phone="0000000000"
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return {
        "message": "User created successfully",
        "id": new_user.id
    }


# UPDATE USER
@router.put("/users/{user_id}")
def update_user(user_id: int, data: dict, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        return {"message": "User not found"}

    user.full_name = data.get("name")
    user.email = data.get("email")
    user.role = data.get("role")
    user.blood_group = data.get("blood")

    db.commit()

    return {
        "message": "User updated successfully"
    }


# UPDATE STATUS
@router.patch("/users/{user_id}/status")
def update_status(user_id: int, data: dict, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        return {"message": "User not found"}

    user.status = data.get("status")

    db.commit()

    return {
        "message": "Status updated"
    }


# DELETE USER
@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        return {"message": "User not found"}

    db.delete(user)
    db.commit()

    return {
        "message": "User deleted successfully"
    }