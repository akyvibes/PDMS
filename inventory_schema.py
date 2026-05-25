from pydantic import BaseModel
from typing import Optional


class InventoryCreate(BaseModel):
    blood_group: str
    units: int


class InventoryUpdate(BaseModel):
    blood_group: Optional[str] = None
    units: Optional[int] = None


class InventoryResponse(BaseModel):
    id: int
    blood_group: str
    units: int
    status: str

    class Config:
        from_attributes = True