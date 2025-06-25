from typing import List, Optional
from health_app.repositories.doctor_repository import DoctorRepository
from health_app.schemas.doctor import Doctor, DoctorCreate, DoctorUpdate


class DoctorService:
    """
    Service layer for doctors.
    Handles business logic and delegates data access to the repository.
    """
    def __init__(self):
        self.repo = DoctorRepository()

    def list_doctors(
        self,
        page: int = 1,
        page_size: int = 10,
        search: Optional[str] = None
    ) -> List[Doctor]:
        # List all doctors with optional filtering and pagination
        return self.repo.get_all(page=page, page_size=page_size, search=search)

    def create_doctor(self, doctor_data: DoctorCreate) -> Doctor:
        # Create a new doctor
        return self.repo.create(doctor_data.dict())

    def get_doctor(self, doctor_id: str) -> Optional[Doctor]:
        # Retrieve a doctor by ID
        return self.repo.get_by_id(doctor_id)

    def update_doctor(self, doctor_id: str, update_data: DoctorUpdate) -> Optional[Doctor]:
        # Update an existing doctor
        return self.repo.update(doctor_id, update_data.dict(exclude_unset=True))

    def delete_doctor(self, doctor_id: str) -> bool:
        # Soft delete a doctor
        return self.repo.soft_delete(doctor_id)

    def get_doctors_by_specialty(self, specialty: str) -> List[Doctor]:
        """
        Retrieve all doctors with a specific specialty.
        """
        return self.repo.get_by_specialty(specialty)

    def get_doctors_by_location(self, location: str) -> List[Doctor]:
        """
        Retrieve all doctors with a specific specialty.
        """
        return self.repo.get_by_location(location)
