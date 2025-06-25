from datetime import datetime
from typing import Optional


class MedicalRecord:
    def __init__(
        self,
        id: str,
        patient_id: str,
        diagnosis: str,
        prescriptions: str,
        treatment_date: datetime,
        doctor_notes: str,
        date_created: datetime,
        date_updated: datetime,
        date_deleted: Optional[datetime] = None,
    ):
        self.id = id
        self.patient_id = patient_id
        self.diagnosis = diagnosis
        self.prescriptions = prescriptions
        self.treatment_date = treatment_date
        self.doctor_notes = doctor_notes
        self.date_created = date_created
        self.date_updated = date_updated
        self.date_deleted = date_deleted

    def to_dict(self):
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "diagnosis": self.diagnosis,
            "prescriptions": self.prescriptions,
            "treatment_date": self.treatment_date.isoformat(),
            "doctor_notes": self.doctor_notes,
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
            diagnosis=data["diagnosis"],
            prescriptions=data["prescriptions"],
            treatment_date=datetime.fromisoformat(data["treatment_date"]),
            doctor_notes=data["doctor_notes"],
            date_created=datetime.fromisoformat(data["date_created"]),
            date_updated=datetime.fromisoformat(data["date_updated"]),
            date_deleted=datetime.fromisoformat(
                data["date_deleted"]) if data["date_deleted"] else None,
        )
