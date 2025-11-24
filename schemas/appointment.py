from pydantic import BaseModel
from typing import Optional, Literal


class AppointmentBase(BaseModel):
    pacienteId: str
    pacienteNombre: str
    propietario: str
    fecha: str
    hora: str
    motivo: str
    estado: Literal['pendiente', 'completada', 'cancelada', 'en-proceso']
    fechaCreacion: Optional[str] = None


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentUpdate(BaseModel):
    pacienteId: Optional[str] = None
    pacienteNombre: Optional[str] = None
    propietario: Optional[str] = None
    fecha: Optional[str] = None
    hora: Optional[str] = None
    motivo: Optional[str] = None
    estado: Optional[Literal['pendiente', 'completada', 'cancelada', 'en-proceso']] = None
    fechaCreacion: Optional[str] = None


class AppointmentInDB(AppointmentBase):
    id: str

    class Config:
        from_attributes = True
