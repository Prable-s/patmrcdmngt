from typing import List, Optional
from health_app.repositories.medical_record_repository import MedicalRecordRepository
from health_app.schemas.medical_record import MedicalRecord, MedicalRecordCreate, MedicalRecordUpdate


class MedicalRecordService:
    """
    Service layer for medical records.
    Handles business logic and delegates data access to the repository.
    """
    def __init__(self):
        self.repo = MedicalRecordRepository()

    def list_medical_records(self, page: int = 1, page_size: int = 10, patient_id: Optional[str] = None) -> List[MedicalRecord]:
        # List all medical records with optional filtering and pagination
        return self.repo.get_all(page=page, page_size=page_size, patient_id=patient_id)

    def create_medical_record(self, record_data: MedicalRecordCreate) -> MedicalRecord:
        # Create a new medical record
        return self.repo.create(record_data.dict())

    def get_medical_record(self, record_id: str) -> Optional[MedicalRecord]:
        # Retrieve a medical record by ID
        return self.repo.get_by_id(record_id)

    def update_medical_record(self, record_id: str, update_data: MedicalRecordUpdate) -> Optional[MedicalRecord]:
        # Update an existing medical record
        return self.repo.update(record_id, update_data.dict(exclude_unset=True))

    def delete_medical_record(self, record_id: str) -> bool:
        # Soft delete a medical record
        return self.repo.soft_delete(record_id)
