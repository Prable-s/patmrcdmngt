from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PatientBase(BaseModel):
    full_name: str
    age: int
    gender: str
    contact_information: str
    address: str
    emergency_contact: str


class PatientCreate(PatientBase):
    pass


class PatientUpdate(PatientBase):
    pass


class Patient(PatientBase):
    id: str
    date_created: datetime
    date_updated: datetime
    date_deleted: Optional[datetime] = None

    class Config:
        orm_mode = True
