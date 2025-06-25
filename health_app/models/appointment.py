from datetime import datetime
from typing import Optional
from enum import Enum


class AppointmentStatus(str, Enum):
    SCHEDULED = "Scheduled"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


class Appointment:
    def __init__(
        self,
        id: str,
        patient_id: str,
        doctor_id: str,
        date_and_time: datetime,
        status: AppointmentStatus,
        date_created: datetime,
        date_updated: datetime,
        date_deleted: Optional[datetime] = None,
    ):
        self.id = id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.date_and_time = date_and_time
        self.status = status
        self.date_created = date_created
        self.date_updated = date_updated
        self.date_deleted = date_deleted

    def to_dict(self):
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "doctor_id": self.doctor_id,
            "date_and_time": self.date_and_time.isoformat(),
            "status": self.status.value,
            "date_created": self.date_created.isoformat(),
            "date_updated": self.date_updated.isoformat(),
            "date_deleted": (
                self.date_deleted.isoformat() if self.date_deleted else None
            ),
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            patient_id=data["patient_id"],
            doctor_id=data["doctor_id"],
            date_and_time=datetime.fromisoformat(data["date_and_time"]),
            status=AppointmentStatus(data["status"]),
            date_created=datetime.fromisoformat(data["date_created"]),
            date_updated=datetime.fromisoformat(data["date_updated"]),
            date_deleted=datetime.fromisoformat(
                data["date_deleted"]) if data["date_deleted"] else None,
        )
