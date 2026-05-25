from pydantic import BaseModel


class CampCreate(BaseModel):

    day: str

    month: str

    title: str

    location: str

    donors: int

    time: str

    type: str

    status: str

    latitude: float

    longitude: float


class CampResponse(CampCreate):

    id: int

    class Config:
        from_attributes = True