from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.audit_model import AuditLog

router = APIRouter()


@router.post("/audit-log")
def create_audit_log(action: str, db: Session = Depends(get_db)):
    new_log = AuditLog(action=action)
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return {
        "message": "Audit log created successfully",
        "log_id": new_log.id
    }


@router.get("/audit-log")
def get_audit_logs(db: Session = Depends(get_db)):
    logs = db.query(AuditLog).all()
    return logs
