from typing import List, Optional
from datetime import datetime
import uuid

from health_app.utils.file_manager import FileManager
from health_app.models.doctor import Doctor


class DoctorRepository:
    def __init__(self, file_path="health_app/data/doctors.json"):
        self.file_manager = FileManager(file_path)
        self.doctors: List[Doctor] = self._load_doctors()

    def _load_doctors(self) -> List[Doctor]:
        data = self.file_manager.read_data()
        return [Doctor.from_dict(doctor_data)
                for doctor_data in data]

    def _save_doctors(self) -> None:
        data = [doctor.to_dict() for doctor in self.doctors]
        self.file_manager.write_data(data)

    def get_all(self, page: int = 1, page_size:
                int = 10, search: Optional[str] = None) -> List[Doctor]:
        start = (page - 1) * page_size
        end = start + page_size

        filtered_doctors = self.doctors
        if search:
            filtered_doctors = [doctor for doctor in filtered_doctors if
                                search.lower() in doctor.full_name.lower()]

        return filtered_doctors[start:end]

    def get_by_id(self, doctor_id: str) -> Optional[Doctor]:
        for doctor in self.doctors:
            if doctor.id == doctor_id and doctor.date_deleted is None:
                return doctor
        return None

    def create(self, doctor_data: dict) -> Doctor:
        doctor_id = str(uuid.uuid4())
        date_created = datetime.now()
        date_updated = date_created
        new_doctor = Doctor(
            id=doctor_id,
            full_name=doctor_data["full_name"],
            specialty=doctor_data["specialty"],
            years_of_experience=doctor_data["years_of_experience"],
            contact_information=doctor_data["contact_information"],
            date_created=date_created,
            date_updated=date_updated,
        )
        self.doctors.append(new_doctor)
        self._save_doctors()
        return new_doctor

    def update(self, doctor_id: str, doctor_data: dict) -> Optional[Doctor]:
        doctor = self.get_by_id(doctor_id)
        if not doctor:
            return None

        doctor.full_name = doctor_data.get("full_name", doctor.full_name)
        doctor.specialty = doctor_data.get("specialty", doctor.specialty)
        doctor.years_of_experience = doctor_data.get(
            "years_of_experience", doctor.years_of_experience)
        doctor.contact_information = doctor_data.get(
            "contact_information", doctor.contact_information)
        doctor.date_updated = datetime.now()

        self._save_doctors()
        return doctor

    def soft_delete(self, doctor_id: str) -> bool:
        doctor = self.get_by_id(doctor_id)
        if not doctor:
            return False

        doctor.date_deleted = datetime.now()
        self._save_doctors()
        return True
