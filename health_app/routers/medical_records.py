from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from health_app.schemas.medical_record import MedicalRecord, MedicalRecordCreate, MedicalRecordUpdate
from health_app.repositories.medical_record_repository import MedicalRecordRepository

router = APIRouter(prefix="/medical_records", tags=["medical_records"])
repo = MedicalRecordRepository()


@router.get("/", response_model=List[MedicalRecord])
def list_medical_records(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    patient_id: Optional[str] = None
):

    return repo.get_all(page=page, page_size=page_size, patient_id=patient_id)


@router.post("/", response_model=MedicalRecord, status_code=201)
def create_medical_record(record: MedicalRecordCreate):

    return repo.create(record.dict())


@router.get("/{record_id}", response_model=MedicalRecord)
def get_medical_record(record_id: str):

    record = repo.get_by_id(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Medical record not found")
    return record


@router.put("/{record_id}", response_model=MedicalRecord)
def update_medical_record(record_id: str, record_update: MedicalRecordUpdate):

    updated = repo.update(record_id, record_update.dict(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Medical record not found")
    return updated


@router.delete("/{record_id}", status_code=204)
def delete_medical_record(record_id: str):

    deleted = repo.soft_delete(record_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Medical record not found")
