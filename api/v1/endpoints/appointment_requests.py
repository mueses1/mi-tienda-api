from datetime import datetime
from typing import List

from fastapi import APIRouter, HTTPException, status

from crud.firebase_crud import FirebaseAppointmentRequestCRUD
from schemas.appointment_request import (
    AppointmentRequestCreate,
    AppointmentRequestInDB,
    AppointmentRequestUpdate,
)

router = APIRouter()

request_crud = FirebaseAppointmentRequestCRUD()


@router.get("/", response_model=List[AppointmentRequestInDB])
def get_all_requests():
    return request_crud.get_all()


@router.get("/{request_id}", response_model=AppointmentRequestInDB)
def get_request(request_id: str):
    req = request_crud.get_by_id(request_id)
    if not req:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    return req


@router.post("/", response_model=AppointmentRequestInDB, status_code=status.HTTP_201_CREATED)
def create_request(request: AppointmentRequestCreate):
    data = request.model_dump()
    # Si no viene creadaEn, registramos ahora
    if not data.get("creadaEn"):
        data["creadaEn"] = datetime.utcnow().isoformat()
    created = request_crud.create(data)
    return created


@router.put("/{request_id}", response_model=AppointmentRequestInDB)
def update_request(request_id: str, request_update: AppointmentRequestUpdate):
    update_data = request_update.model_dump(exclude_unset=True)
    updated = request_crud.update(request_id, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    return updated


@router.delete("/{request_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_request(request_id: str):
    deleted = request_crud.delete(request_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    return None
