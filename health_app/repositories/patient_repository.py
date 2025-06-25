from typing import List, Optional
from datetime import datetime
import uuid

from health_app.utils.file_manager import FileManager
from health_app.models.patient import Patient


class PatientRepository:
    def __init__(self, file_path="health_app/data/patients.json"):
        self.file_manager = FileManager(file_path)
        self.patients: List[Patient] = self._load_patients()

    def _load_patients(self) -> List[Patient]:
        data = self.file_manager.read_data()
        return [
            Patient.from_dict(patient_data)
            for patient_data in data
        ]

    def _save_patients(self) -> None:
        data = [patient.to_dict() for patient in self.patients]
        self.file_manager.write_data(data)

    def get_all(self, page: int = 1, page_size:
                int = 10, search: Optional[str] = None) -> List[Patient]:
        start = (page - 1) * page_size
        end = start + page_size

        filtered_patients = self.patients
        if search:
            filtered_patients = [
                p
                for p in filtered_patients
                if search.lower() in p.full_name.lower()
            ]

        return filtered_patients[start:end]

    def get_by_id(self, patient_id: str) -> Optional[Patient]:
        for patient in self.patients:
            if patient.id == patient_id and patient.date_deleted is None:
                return patient
        return None

    def create(self, patient_data: dict) -> Patient:
        patient_id = str(uuid.uuid4())
        date_created = datetime.now()
        date_updated = date_created
        new_patient = Patient(
            id=patient_id,
            full_name=patient_data["full_name"],
            age=patient_data["age"],
            gender=patient_data["gender"],
            contact_information=patient_data["contact_information"],
            address=patient_data["address"],
            emergency_contact=patient_data["emergency_contact"],
            date_created=date_created,
            date_updated=date_updated,
        )
        self.patients.append(new_patient)
        self._save_patients()
        return new_patient

    def update(self, patient_id: str, patient_data: dict) -> Optional[Patient]:
        patient = self.get_by_id(patient_id)
        if not patient:
            return None

        patient.full_name = patient_data.get("full_name", patient.full_name)
        patient.age = patient_data.get("age", patient.age)
        patient.gender = patient_data.get("gender", patient.gender)
        patient.contact_information = patient_data.get(
            "contact_information", patient.contact_information
        )
        patient.address = patient_data.get("address", patient.address)
        patient.emergency_contact = patient_data.get(
            "emergency_contact", patient.emergency_contact
        )
        patient.date_updated = datetime.now()

        self._save_patients()
        return patient

    def soft_delete(self, patient_id: str) -> bool:
        patient = self.get_by_id(patient_id)
        if not patient:
            return False

        patient.date_deleted = datetime.now()
        self._save_patients()
        return True
