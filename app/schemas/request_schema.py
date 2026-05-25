from pydantic import BaseModel

class RequestCreate(BaseModel):
    patient_name: str
    blood_group: str
    hospital: str
    units: int

class RequestUpdate(BaseModel):
    patient_name: str | None = None
    blood_group: str | None = None
    hospital: str | None = None
    units: int | None = None
    status: str | None = None