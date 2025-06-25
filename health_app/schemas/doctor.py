from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class DoctorBase(BaseModel):
    full_name: str
    specialty: str
    years_of_experience: int
    contact_information: str


class DoctorCreate(DoctorBase):
    pass


class DoctorUpdate(DoctorBase):
    pass


class Doctor(DoctorBase):
    id: str
    date_created: datetime
    date_updated: datetime
    date_deleted: Optional[datetime] = None

    class Config:
        orm_mode = True
