from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.request_model import BloodRequest
from app.schemas.request_schema import RequestCreate, RequestUpdate

router = APIRouter()

# CREATE REQUEST
@router.post("/requests")
def create_request(request: RequestCreate, db: Session = Depends(get_db)):
    new_request = BloodRequest(
        patient_name=request.patient_name,
        blood_group=request.blood_group,
        hospital=request.hospital,
        units=request.units,
        status="pending"
    )
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    return {
        "message": "Blood request created successfully",
        "request_id": new_request.id
    }


@router.get("/requests")
def get_requests(db: Session = Depends(get_db)):
    requests = db.query(BloodRequest).all()
    return requests


@router.put("/requests/{request_id}")
def update_request(
    request_id: int,
    request_update: RequestUpdate,
    db: Session = Depends(get_db)
):
    request_record = db.query(BloodRequest).filter(
        BloodRequest.id == request_id
    ).first()
    if not request_record:
        raise HTTPException(status_code=404, detail="Request not found")

    if request_update.patient_name is not None:
        request_record.patient_name = request_update.patient_name
    if request_update.blood_group is not None:
        request_record.blood_group = request_update.blood_group
    if request_update.hospital is not None:
        request_record.hospital = request_update.hospital
    if request_update.units is not None:
        request_record.units = request_update.units
    if request_update.status is not None:
        request_record.status = request_update.status

    db.commit()
    db.refresh(request_record)
    return {
        "message": "Request updated successfully",
        "request": request_record
    }


@router.delete("/requests/{request_id}")
def delete_request(request_id: int, db: Session = Depends(get_db)):
    request_record = db.query(BloodRequest).filter(
        BloodRequest.id == request_id
    ).first()
    if not request_record:
        raise HTTPException(status_code=404, detail="Request not found")

    db.delete(request_record)
    db.commit()
    return {"message": "Request deleted successfully"}


@router.put("/accept-request/{request_id}")
def accept_request(request_id: int, db: Session = Depends(get_db)):
    request_record = db.query(BloodRequest).filter(
        BloodRequest.id == request_id
    ).first()
    if not request_record:
        raise HTTPException(status_code=404, detail="Request not found")

    request_record.status = "accepted"
    db.commit()
    db.refresh(request_record)
    return {
        "message": "Request accepted successfully",
        "request": request_record
    }
