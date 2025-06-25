# import os
from typing import List, Optional
from datetime import datetime
import uuid

from health_app.utils.file_manager import FileManager
from health_app.models.appointment import Appointment, AppointmentStatus


class AppointmentRepository:
    def __init__(self, file_path="health_app/data/appointments.json"):
        self.file_manager = FileManager(file_path)
        self.appointments: List[Appointment] = self._load_appointments()

    def _load_appointments(self) -> List[Appointment]:
        data = self.file_manager.read_data()
        return [Appointment.from_dict(appointment_data)
                for appointment_data in data]

    def _save_appointments(self) -> None:
        data = [appointment.to_dict() for appointment in self.appointments]
        self.file_manager.write_data(data)

    def get_all(self, page: int = 1, page_size:
                int = 10, status:
                    Optional[AppointmentStatus] = None) -> List[Appointment]:
        start = (page - 1) * page_size
        end = start + page_size

        filtered_appointments = self.appointments
        if status:
            filtered_appointments = [
                appointment for appointment in filtered_appointments
                if appointment.status == status
            ]

        return filtered_appointments[start:end]

    def get_by_id(self, appointment_id: str) -> Optional[Appointment]:
        for appointment in self.appointments:
            if (appointment.id == appointment_id and
                    appointment.date_deleted is None):
                return appointment
        return None

    def create(self, appointment_data: dict) -> Appointment:
        appointment_id = str(uuid.uuid4())
        date_created = datetime.now()
        date_updated = date_created
        new_appointment = Appointment(
            id=appointment_id,
            patient_id=appointment_data["patient_id"],
            doctor_id=appointment_data["doctor_id"],
            date_and_time=appointment_data["date_and_time"],
            status=AppointmentStatus(appointment_data["status"]),
            date_created=date_created,
            date_updated=date_updated,
        )
        self.appointments.append(new_appointment)
        self._save_appointments()
        return new_appointment

    def update(self, appointment_id: str, appointment_data: dict) -> Optional[
                                            Appointment]:
        appointment = self.get_by_id(appointment_id)
        if not appointment:
            return None

        appointment.patient_id = appointment_data.get(
            "patient_id", appointment.patient_id)
        appointment.doctor_id = appointment_data.get(
            "doctor_id", appointment.doctor_id)
        appointment.date_and_time = appointment_data.get(
            "date_and_time", appointment.date_and_time)
        appointment.status = AppointmentStatus(appointment_data.get(
            "status", appointment.status))
        appointment.date_updated = datetime.now()

        self._save_appointments()
        return appointment

    def soft_delete(self, appointment_id: str) -> bool:
        appointment = self.get_by_id(appointment_id)
        if not appointment:
            return False

        appointment.date_deleted = datetime.now()
        self._save_appointments()
        return True
