from pydantic import BaseModel, EmailStr
from typing import Optional, Literal


class AppointmentRequestBase(BaseModel):
    nombrePropietario: str
    nombreMascota: str
    telefono: str
    email: EmailStr
    motivo: str
    estado: Literal['pendiente', 'gestionada', 'rechazada'] = 'pendiente'
    creadaEn: Optional[str] = None


class AppointmentRequestCreate(AppointmentRequestBase):
    pass


class AppointmentRequestUpdate(BaseModel):
    nombrePropietario: Optional[str] = None
    nombreMascota: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[EmailStr] = None
    motivo: Optional[str] = None
    estado: Optional[Literal['pendiente', 'gestionada', 'rechazada']] = None
    creadaEn: Optional[str] = None


class AppointmentRequestInDB(AppointmentRequestBase):
    id: str

    class Config:
        from_attributes = True
