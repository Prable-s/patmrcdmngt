from typing import List, Optional
from health_app.repositories.appointment_repository import AppointmentRepository
from health_app.schemas.appointment import Appointment, AppointmentCreate, AppointmentUpdate


class AppointmentService:
    """
    Service layer for appointments.
    Handles business logic and delegates data access to the repository.
    """
    def __init__(self):
        self.repo = AppointmentRepository()

    def list_appointments(
        self,
        page: int = 1,
        page_size: int = 10,
        status: Optional[str] = None,
        doctor_id: Optional[str] = None,
        patient_id: Optional[str] = None
    ) -> List[Appointment]:
        # List all appointments with optional filtering and pagination
        return self.repo.get_all(
            page=page,
            page_size=page_size,
            status=status,
            doctor_id=doctor_id,
            patient_id=patient_id
        )

    def create_appointment(self, appointment_data: AppointmentCreate) -> Appointment:
        # Create a new appointment, enforcing business rules (e.g., no double-booking)
        return self.repo.create(appointment_data.dict())

    def get_appointment(self, appointment_id: str) -> Optional[Appointment]:
        # Retrieve an appointment by ID
        return self.repo.get_by_id(appointment_id)

    def update_appointment(self, appointment_id: str, update_data: AppointmentUpdate) -> Optional[Appointment]:
        # Update an existing appointment
        return self.repo.update(appointment_id, update_data.dict(
            exclude_unset=True))

    def delete_appointment(self, appointment_id: str) -> bool:
        # Soft delete an appointment
        return self.repo.soft_delete(appointment_id)

    def get_appointments_by_patient(self, patient_id: str) -> List[Appointment]:
        """
        Retrieve all appointments for a specific patient.
        """
        return self.repo.get_by_patient(patient_id)
