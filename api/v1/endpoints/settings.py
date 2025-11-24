from fastapi import APIRouter
from schemas.settings import SettingsInDB, SettingsBase, SettingsUpdate, ClinicaConfig, NotificacionesConfig, SistemaConfig, SeguridadConfig
from crud.firebase_crud import FirebaseSettingsCRUD


router = APIRouter()

settings_crud = FirebaseSettingsCRUD()


def _default_settings() -> SettingsInDB:
    return SettingsInDB(
        clinica=ClinicaConfig(
            nombre="VetClinic Pro",
            direccion="Av. Principal 123, Ciudad",
            telefono="(555) 123-4567",
            email="info@vetclinic.com",
            horarioApertura="08:00",
            horarioCierre="18:00",
            diasLaborales=["lunes", "martes", "miercoles", "jueves", "viernes", "sabado"],
        ),
        notificaciones=NotificacionesConfig(
            emailNuevoPaciente=True,
            emailNuevaCita=True,
            recordatoriosCitas=True,
            reportesDiarios=False,
            alertasVacunacion=True,
        ),
        sistema=SistemaConfig(
            tema="claro",
            idioma="es",
            formatoFecha="dd/mm/yyyy",
            formatoHora="24h",
            autoguardado=True,
            backupAutomatico=True,
        ),
        seguridad=SeguridadConfig(
            sesionExpira="8",
            requiereCambioPassword=False,
            autenticacionDosFactor=False,
            logActividades=True,
        ),
    )


@router.get("/", response_model=SettingsInDB)
def get_settings():
    data = settings_crud.get()
    if not data:
        # Si no existe configuración, devolvemos los valores por defecto
        return _default_settings()
    return SettingsInDB(**data)


@router.put("/", response_model=SettingsInDB)
def update_settings(payload: SettingsUpdate):
    update_data = payload.model_dump(exclude_unset=True)

    # Siempre partimos de los valores por defecto completos
    base = _default_settings().model_dump()

    # Obtener la configuración actual (si existe). Puede ser parcial.
    current = settings_crud.get() or {}

    # Orden de prioridad: defaults < lo que ya hay en Firestore < lo que llega en el payload
    merged = {**base, **current, **update_data}

    # Guardar configuración fusionada en Firestore (merge=True ya se maneja en el CRUD)
    saved = settings_crud.upsert(merged)

    # Aseguramos que el modelo tenga todas las secciones requeridas
    return SettingsInDB(**saved)
