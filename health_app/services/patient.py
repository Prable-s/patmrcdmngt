from typing import List, Optional
from health_app.repositories.patient_repository import PatientRepository
from health_app.schemas.patient import Patient, PatientCreate, PatientUpdate


class PatientService:
    """
    Service layer for patients.
    Handles business logic and delegates data access to the repository.
    """
    def __init__(self):
        self.repo = PatientRepository()

    def list_patients(
        self,
        page: int = 1,
        page_size: int = 10,
        search: Optional[str] = None
    ) -> List[Patient]:
        # List all patients with optional filtering and pagination
        return self.repo.get_all(page=page, page_size=page_size, search=search)

    def create_patient(self, patient_data: PatientCreate) -> Patient:
        # Create a new patient
        return self.repo.create(patient_data.dict())

    def get_patient(self, patient_id: str) -> Optional[Patient]:
        # Retrieve a patient by ID
        return self.repo.get_by_id(patient_id)

    def update_patient(self, patient_id: str, update_data: PatientUpdate) -> Optional[Patient]:
        # Update an existing patient
        return self.repo.update(patient_id, update_data.dict(exclude_unset=True))

    def delete_patient(self, patient_id: str) -> bool:
        # Soft delete a patient
        return self.repo.soft_delete(patient_id)
