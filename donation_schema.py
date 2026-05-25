from pydantic import BaseModel

class DonationCreate(BaseModel):
    donor_email: str
    date: str
    center: str
    type: str
    status: str

class DonationResponse(DonationCreate):
    id: int

    class Config:
        from_attributes = True