# import os
from typing import List, Optional
from datetime import datetime
import uuid

from health_app.utils.file_manager import FileManager
from health_app.models.medical_record import MedicalRecord


class MedicalRecordRepository:
    def __init__(self, file_path="health_app/data/medical_records.json"):
        self.file_manager = FileManager(file_path)
        self.medical_records: List[
            MedicalRecord] = self._load_medical_records()

    def _load_medical_records(self) -> List[MedicalRecord]:
        data = self.file_manager.read_data()
        return [MedicalRecord.from_dict(medical_record_data)
                for medical_record_data in data]

    def _save_medical_records(self) -> None:
        data = [medical_record.to_dict()
                for medical_record in self.medical_records]
        self.file_manager.write_data(data)

    def get_all(self) -> List[MedicalRecord]:
        return self.medical_records

    def get_by_id(self, medical_record_id: str) -> Optional[MedicalRecord]:
        for medical_record in self.medical_records:
            if (medical_record.id == medical_record_id and
                    medical_record.date_deleted is None):
                return medical_record
        return None

    def create(self, medical_record_data: dict) -> MedicalRecord:
        medical_record_id = str(uuid.uuid4())
        date_created = datetime.now()
        date_updated = date_created
        new_medical_record = MedicalRecord(
            id=medical_record_id,
            patient_id=medical_record_data["patient_id"],
            diagnosis=medical_record_data["diagnosis"],
            prescriptions=medical_record_data["prescriptions"],
            treatment_date=medical_record_data["treatment_date"],
            doctor_notes=medical_record_data["doctor_notes"],
            date_created=date_created,
            date_updated=date_updated,
        )
        self.medical_records.append(new_medical_record)
        self._save_medical_records()
        return new_medical_record

    def update(self, medical_record_id: str,
               medical_record_data: dict) -> Optional[MedicalRecord]:
        medical_record = self.get_by_id(medical_record_id)
        if not medical_record:
            return None

        medical_record.patient_id = medical_record_data.get(
            "patient_id", medical_record.patient_id)
        medical_record.diagnosis = medical_record_data.get(
            "diagnosis", medical_record.diagnosis)
        medical_record.prescriptions = medical_record_data.get(
            "prescriptions", medical_record.prescriptions)
        medical_record.treatment_date = medical_record_data.get(
            "treatment_date", medical_record.treatment_date)
        medical_record.doctor_notes = medical_record_data.get(
            "doctor_notes", medical_record.doctor_notes)
        medical_record.date_updated = datetime.now()

        self._save_medical_records()
        return medical_record

    def soft_delete(self, medical_record_id: str) -> bool:
        medical_record = self.get_by_id(medical_record_id)
        if not medical_record:
            return False

        medical_record.date_deleted = datetime.now()
        self._save_medical_records()
        return True
