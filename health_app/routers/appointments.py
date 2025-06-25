from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from health_app.schemas.appointment import Appointment
from health_app.schemas.appointment import AppointmentCreate, AppointmentUpdate
from health_app.repositories.appointment_repository import AppointmentRepository

router = APIRouter(prefix="/appointments", tags=["appointments"])
repo = AppointmentRepository()


@router.get("/", response_model=List[Appointment])
def list_appointments(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    status: Optional[str] = None,
    doctor_id: Optional[str] = None,
    patient_id: Optional[str] = None
):

    return repo.get_all(page=page, page_size=page_size,
                        status=status, doctor_id=doctor_id,
                        patient_id=patient_id)


@router.post("/", response_model=Appointment, status_code=201)
def create_appointment(appointment: AppointmentCreate):

    try:
        return repo.create(appointment.dict())
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get("/{appointment_id}", response_model=Appointment)
def get_appointment(appointment_id: str):

    appointment = repo.get_by_id(appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment


@router.put("/{appointment_id}", response_model=Appointment)
def update_appointment(appointment_id: str,
                       appointment_update: AppointmentUpdate):

    try:
        updated = repo.update(appointment_id,
                              appointment_update.dict(exclude_unset=True))
        if not updated:
            raise HTTPException(status_code=404,
                                detail="Appointment not found")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.delete("/{appointment_id}", status_code=204)
def delete_appointment(appointment_id: str):

    deleted = repo.soft_delete(appointment_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return {"detail": "Appointment deleted successfully"}
