from pydantic import BaseModel
from typing import List, Optional


class ClinicaConfig(BaseModel):
    nombre: str
    direccion: str
    telefono: str
    email: str
    horarioApertura: str
    horarioCierre: str
    diasLaborales: List[str]


class NotificacionesConfig(BaseModel):
    emailNuevoPaciente: bool
    emailNuevaCita: bool
    recordatoriosCitas: bool
    reportesDiarios: bool
    alertasVacunacion: bool


class SistemaConfig(BaseModel):
    tema: str
    idioma: str
    formatoFecha: str
    formatoHora: str
    autoguardado: bool
    backupAutomatico: bool


class SeguridadConfig(BaseModel):
    sesionExpira: str
    requiereCambioPassword: bool
    autenticacionDosFactor: bool
    logActividades: bool


class SettingsBase(BaseModel):
    clinica: ClinicaConfig
    notificaciones: NotificacionesConfig
    sistema: SistemaConfig
    seguridad: SeguridadConfig


class ClinicaConfigUpdate(BaseModel):
    nombre: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    horarioApertura: Optional[str] = None
    horarioCierre: Optional[str] = None
    diasLaborales: Optional[List[str]] = None


class NotificacionesConfigUpdate(BaseModel):
    emailNuevoPaciente: Optional[bool] = None
    emailNuevaCita: Optional[bool] = None
    recordatoriosCitas: Optional[bool] = None
    reportesDiarios: Optional[bool] = None
    alertasVacunacion: Optional[bool] = None


class SistemaConfigUpdate(BaseModel):
    tema: Optional[str] = None
    idioma: Optional[str] = None
    formatoFecha: Optional[str] = None
    formatoHora: Optional[str] = None
    autoguardado: Optional[bool] = None
    backupAutomatico: Optional[bool] = None


class SeguridadConfigUpdate(BaseModel):
    sesionExpira: Optional[str] = None
    requiereCambioPassword: Optional[bool] = None
    autenticacionDosFactor: Optional[bool] = None
    logActividades: Optional[bool] = None


class SettingsUpdate(BaseModel):
    clinica: Optional[ClinicaConfigUpdate] = None
    notificaciones: Optional[NotificacionesConfigUpdate] = None
    sistema: Optional[SistemaConfigUpdate] = None
    seguridad: Optional[SeguridadConfigUpdate] = None


class SettingsInDB(SettingsBase):
    class Config:
        from_attributes = True
