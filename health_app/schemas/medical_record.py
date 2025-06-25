from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class MedicalRecordBase(BaseModel):
    patient_id: str
    diagnosis: str
    prescriptions: str
    treatment_date: datetime
    doctor_notes: str


class MedicalRecordCreate(MedicalRecordBase):
    pass


class MedicalRecordUpdate(MedicalRecordBase):
    pass


class MedicalRecord(MedicalRecordBase):
    id: str
    date_created: datetime
    date_updated: datetime
    date_deleted: Optional[datetime] = None

    class Config:
        orm_mode = True
