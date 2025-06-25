from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

from health_app.schemas.doctor import Doctor, DoctorCreate, DoctorUpdate
from health_app.repositories.doctor_repository import DoctorRepository

router = APIRouter(prefix="/doctors", tags=["doctors"])
repo = DoctorRepository()


@router.get("/", response_model=List[Doctor])
def list_doctors(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    search: Optional[str] = None
):
    """
    List all doctors (excluding deleted) with pagination and
    optional name search.
    """
    return repo.get_all(page=page, page_size=page_size, search=search)


@router.post("/", response_model=Doctor, status_code=201)
def create_doctor(doctor: DoctorCreate):
    """
    Create a new doctor.
    """
    return repo.create(doctor.dict())


@router.get("/{doctor_id}", response_model=Doctor)
def get_Doctor(doctor_id: str):
    """
    Retrieve doctor details by ID.
    """
    doctor = repo.get_by_id(doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="doctor not found")
    return doctor


@router.put("/{doctor_id}", response_model=Doctor)
def update_doctor(doctor_id: str, doctor_update: DoctorUpdate):
    """
    Update doctor information.
    """
    updated = repo.update(doctor_id, doctor_update.dict(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="doctor not found")
    return updated


@router.delete("/{doctor_id}", status_code=204)
def delete_doctor(doctor_id: str):
    """
    Soft delete a doctor.
    """
    deleted = repo.soft_delete(doctor_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return {"detail": "Doctor deleted successfully"}
