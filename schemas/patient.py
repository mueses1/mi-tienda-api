from pydantic import BaseModel
from typing import Optional


class PatientBase(BaseModel):
    # Campos legacy usados en el frontend actual
    nombre: str  # nombre de la mascota (para compatibilidad)
    propietario: str  # nombre completo del tutor (para compatibilidad)
    email: str
    fecha: str  # fecha de registro o alta
    sintomas: str

    # Datos del tutor (dueño)
    tutor_nombre: Optional[str] = None
    tutor_apellido: Optional[str] = None
    tutor_tipo_documento: Optional[str] = None
    tutor_numero_documento: Optional[str] = None
    tutor_telefono_principal: Optional[str] = None
    tutor_telefono_secundario: Optional[str] = None
    tutor_email: Optional[str] = None
    tutor_direccion: Optional[str] = None
    tutor_como_nos_conocio: Optional[str] = None

    # Datos del paciente (mascota)
    mascota_nombre: Optional[str] = None
    mascota_especie: Optional[str] = None
    mascota_raza: Optional[str] = None
    mascota_raza_otro: Optional[str] = None
    mascota_sexo: Optional[str] = None
    mascota_castrado: Optional[str] = None  # 'si' | 'no' | 'no_sabe'
    mascota_edad_aproximada_anios: Optional[int] = None
    mascota_color: Optional[str] = None
    mascota_peso_kg: Optional[float] = None
    mascota_foto_url: Optional[str] = None

    # Información médica importante
    enfermedad_cronica: Optional[str] = None
    medicacion_permanente: Optional[str] = None
    alergias: Optional[str] = None
    tiene_seguro_medico: Optional[bool] = None
    nombre_aseguradora: Optional[str] = None
    observaciones: Optional[str] = None


class PatientCreate(PatientBase):
    pass


class PatientUpdate(BaseModel):
    nombre: Optional[str] = None
    propietario: Optional[str] = None
    email: Optional[str] = None
    fecha: Optional[str] = None
    sintomas: Optional[str] = None

    tutor_nombre: Optional[str] = None
    tutor_apellido: Optional[str] = None
    tutor_tipo_documento: Optional[str] = None
    tutor_numero_documento: Optional[str] = None
    tutor_telefono_principal: Optional[str] = None
    tutor_telefono_secundario: Optional[str] = None
    tutor_email: Optional[str] = None
    tutor_direccion: Optional[str] = None
    tutor_como_nos_conocio: Optional[str] = None

    mascota_nombre: Optional[str] = None
    mascota_especie: Optional[str] = None
    mascota_raza: Optional[str] = None
    mascota_raza_otro: Optional[str] = None
    mascota_sexo: Optional[str] = None
    mascota_castrado: Optional[str] = None
    mascota_edad_aproximada_anios: Optional[int] = None
    mascota_color: Optional[str] = None
    mascota_peso_kg: Optional[float] = None
    mascota_foto_url: Optional[str] = None

    enfermedad_cronica: Optional[str] = None
    medicacion_permanente: Optional[str] = None
    alergias: Optional[str] = None
    tiene_seguro_medico: Optional[bool] = None
    nombre_aseguradora: Optional[str] = None
    observaciones: Optional[str] = None


class PatientInDB(PatientBase):
    id: str

    class Config:
        from_attributes = True
