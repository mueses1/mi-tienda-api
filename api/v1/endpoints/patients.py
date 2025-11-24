from fastapi import APIRouter, HTTPException, status
from typing import List
from schemas.patient import PatientInDB, PatientCreate, PatientUpdate
from crud.firebase_crud import FirebasePatientCRUD


router = APIRouter()

patient_crud = FirebasePatientCRUD()


@router.get("/", response_model=List[PatientInDB])
def get_all_patients():
    return patient_crud.get_all()


@router.get("/{patient_id}", response_model=PatientInDB)
def get_patient(patient_id: str):
    patient = patient_crud.get_by_id(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return patient


@router.post("/", response_model=PatientInDB, status_code=status.HTTP_201_CREATED)
def create_patient(patient: PatientCreate):
    new_patient = patient_crud.create(patient.model_dump())
    return new_patient


@router.put("/{patient_id}", response_model=PatientInDB)
def update_patient(patient_id: str, patient_update: PatientUpdate):
    update_data = patient_update.model_dump(exclude_unset=True)
    updated = patient_crud.update(patient_id, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return updated


@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(patient_id: str):
    deleted = patient_crud.delete(patient_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return None
