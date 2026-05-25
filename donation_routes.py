from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.donation_model import Donation
from app.schemas.donation_schema import DonationCreate
from app.routes.user_routes import get_current_user

router = APIRouter()

# CREATE DONATION
@router.post("/donations")
def create_donation(
    donation: DonationCreate,
    db: Session = Depends(get_db)
):
    new_donation = Donation(
        current_user = Depends(get_current_user),
        donor_email = get_current_user().email,
        date=donation.date,
        center=donation.center,
        type=donation.type,
        status=donation.status
    )
    db.add(new_donation)
    db.commit()
    db.refresh(new_donation)
    return new_donation

# GET MY DONATION HISTORY
@router.get("/donations/my-history")
def get_my_history(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    donations = db.query(Donation).filter(
        Donation.donor_email == current_user.email
    ).all()
    return donations
