from fastapi import APIRouter, HTTPException, status
from typing import List
from datetime import datetime, time as dt_time
from schemas.appointment import AppointmentInDB, AppointmentCreate, AppointmentUpdate
from crud.firebase_crud import FirebaseAppointmentCRUD


router = APIRouter()

appointment_crud = FirebaseAppointmentCRUD()


@router.get("/", response_model=List[AppointmentInDB])
def get_all_appointments():
    return appointment_crud.get_all()


@router.get("/{appointment_id}", response_model=AppointmentInDB)
def get_appointment(appointment_id: str):
    appointment = appointment_crud.get_by_id(appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    return appointment


@router.post("/", response_model=AppointmentInDB, status_code=status.HTTP_201_CREATED)
def create_appointment(appointment: AppointmentCreate):
    """Crear una cita aplicando reglas de negocio básicas."""

    # Validar formato de fecha y hora y evitar citas en el pasado
    try:
        appointment_dt = datetime.fromisoformat(f"{appointment.fecha}T{appointment.hora}")
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Fecha u hora inválida",
        )

    if appointment_dt < datetime.now():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pueden agendar citas en el pasado",
        )

    # Validar horario de atención (ejemplo: 08:00 a 20:00)
    inicio_jornada = dt_time(8, 0)
    fin_jornada = dt_time(20, 0)
    hora_cita = appointment_dt.time()

    if not (inicio_jornada <= hora_cita <= fin_jornada):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La hora de la cita debe estar entre 08:00 y 20:00",
        )

    # Evitar doble reserva en misma fecha y hora (para cualquier paciente que no esté cancelada)
    existing_appointments = appointment_crud.get_all()
    for existing in existing_appointments:
        if (
            existing.get("fecha") == appointment.fecha
            and existing.get("hora") == appointment.hora
            and existing.get("estado") != "cancelada"
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe una cita programada en esa fecha y hora",
            )

    new_appointment = appointment_crud.create(appointment.model_dump())
    return new_appointment


@router.put("/{appointment_id}", response_model=AppointmentInDB)
def update_appointment(appointment_id: str, appointment_update: AppointmentUpdate):
    update_data = appointment_update.model_dump(exclude_unset=True)
    updated = appointment_crud.update(appointment_id, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    return updated


@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_appointment(appointment_id: str):
    deleted = appointment_crud.delete(appointment_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    return None
