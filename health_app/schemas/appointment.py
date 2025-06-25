from datetime import datetime
from typing import Optional
from enum import Enum

from pydantic import BaseModel


class AppointmentStatus(str, Enum):
    SCHEDULED = "Scheduled"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


class AppointmentBase(BaseModel):
    patient_id: str
    doctor_id: str
    date_and_time: datetime
    status: AppointmentStatus


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentUpdate(AppointmentBase):
    pass


class Appointment(AppointmentBase):
    id: str
    date_created: datetime
    date_updated: datetime
    date_deleted: Optional[datetime] = None

    class Config:
        orm_mode = True
