from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.notification_model import Notification

router = APIRouter()

# CREATE NOTIFICATION
@router.post("/notifications")
def create_notification(
    message: str,
    type: str,
    db: Session = Depends(get_db)
):
    new_notification = Notification(
        message=message,
        type=type
    )
    db.add(new_notification)
    db.commit()
    db.refresh(new_notification)
    return new_notification

# GET ALL NOTIFICATIONS
@router.get("/notifications")
def get_notifications(db: Session = Depends(get_db)):
    notifications = db.query(Notification).all()
    return notifications


@router.delete("/notifications/{notification_id}")
def delete_notification(notification_id: int, db: Session = Depends(get_db)):
    notification = db.query(Notification).filter(
        Notification.id == notification_id
    ).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")

    db.delete(notification)
    db.commit()
    return {"message": "Notification deleted successfully"}
