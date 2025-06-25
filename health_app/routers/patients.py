from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

from health_app.schemas.patient import Patient, PatientCreate, PatientUpdate
from health_app.repositories.patient_repository import PatientRepository

router = APIRouter(prefix="/patients", tags=["patients"])
repo = PatientRepository()


@router.get("/", response_model=List[Patient])
def list_patients(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    search: Optional[str] = None
):
    """
    List all patients (excluding deleted) with pagination and
    optional name search.
    """
    return repo.get_all(page=page, page_size=page_size, search=search)


@router.post("/", response_model=Patient, status_code=201)
def create_patient(patient: PatientCreate):
    """
    Create a new patient.
    """
    return repo.create(patient.dict())


@router.get("/{patient_id}", response_model=Patient)
def get_patient(patient_id: str):
    """
    Retrieve patient details by ID.
    """
    patient = repo.get_by_id(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@router.put("/{patient_id}", response_model=Patient)
def update_patient(patient_id: str, patient_update: PatientUpdate):
    """
    Update patient information.
    """
    updated = repo.update(patient_id, patient_update.dict(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Patient not found")
    return updated


@router.delete("/{patient_id}", status_code=204)
def delete_patient(patient_id: str):
    """
    Soft delete a patient.
    """
    deleted = repo.soft_delete(patient_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"detail": "Patient deleted successfully"}
