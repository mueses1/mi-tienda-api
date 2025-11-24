from fastapi import APIRouter, HTTPException, status, BackgroundTasks
from typing import List
from datetime import datetime, time as dt_time
import smtplib
from email.mime.text import MIMEText

from schemas.appointment import AppointmentInDB, AppointmentCreate, AppointmentUpdate
from crud.firebase_crud import FirebaseAppointmentCRUD, FirebasePatientCRUD
from core.config import settings

router = APIRouter()

appointment_crud = FirebaseAppointmentCRUD()
patient_crud = FirebasePatientCRUD()


def send_appointment_email(to_email: str, appointment: dict) -> None:
    """Envía un correo simple de confirmación de cita.

    Usa configuración SMTP definida en variables de entorno. Si falta
    configuración o se produce un error, se ignora silenciosamente.
    """

    if not (settings.SMTP_HOST and settings.SMTP_USER and settings.SMTP_PASSWORD and settings.SMTP_FROM):
        return

    subject = f"Confirmación de cita para {appointment.get('pacienteNombre', '')}"
    fecha = appointment.get("fecha", "")
    hora = appointment.get("hora", "")
    motivo = appointment.get("motivo", "")
    propietario = appointment.get("propietario", "")

    # Formatear hora a formato AM/PM si es posible (por ejemplo 10:00 AM)
    hora_am_pm = hora
    try:
        if hora:
            from datetime import datetime as _dt

            parsed_time = _dt.strptime(hora, "%H:%M")
            hora_am_pm = parsed_time.strftime("%I:%M %p") 
    except Exception:
        # Si falla el parseo, se deja la hora original
        hora_am_pm = hora

    body = f"""
    <html>
      <head>
        <meta charset="UTF-8" />
        <style>
          body {{ font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background-color: #f5f7fb; margin: 0; padding: 0; }}
          .container {{ max-width: 560px; margin: 24px auto; background: #ffffff; border-radius: 12px; box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08); overflow: hidden; }}
          .header {{ background: linear-gradient(135deg, #2563eb, #1d4ed8); color: #ffffff; padding: 20px 24px; }}
          .header h1 {{ margin: 0; font-size: 20px; font-weight: 700; }}
          .content {{ padding: 24px; color: #0f172a; font-size: 14px; line-height: 1.6; }}
          .content p {{ margin: 0 0 12px 0; }}
          .card {{ background-color: #f9fafb; border-radius: 10px; padding: 16px 18px; margin: 12px 0 20px 0; border: 1px solid #e5e7eb; }}
          .card-title {{ font-weight: 600; margin-bottom: 8px; color: #111827; }}
          .row {{ display: flex; justify-content: space-between; margin-bottom: 6px; }}
          .label {{ font-weight: 500; color: #6b7280; margin-right: 8px; }}
          .value {{ font-weight: 600; color: #111827; }}
          .footer {{ padding: 18px 24px 22px 24px; border-top: 1px solid #e5e7eb; font-size: 12px; color: #6b7280; background-color: #f9fafb; }}
        </style>
      </head>
      <body>
        <div class="container">
          <div class="header">
            <h1>Confirmación de cita</h1>
          </div>
          <div class="content">
            <p>Hola <strong>{propietario}</strong>,</p>
            <p>
              Hemos registrado una cita para tu mascota <strong>{appointment.get('pacienteNombre', '')}</strong> con la siguiente información:
            </p>
            <div class="card">
              <div class="card-title">Detalles de la cita</div>
              <div class="row">
                <span class="label">Fecha</span>
                <span class="value">{fecha}</span>
              </div>
              <div class="row">
                <span class="label">Hora</span>
                <span class="value">{hora_am_pm}</span>
              </div>
              <div class="row">
                <span class="label">Motivo</span>
                <span class="value">{motivo}</span>
              </div>
            </div>
            <p>
              Si necesitas <strong>modificar</strong> o <strong>cancelar</strong> la cita, por favor contacta con nuestra clínica por nuestros canales habituales.
            </p>
            <p>
              Cc:3134026363 o al correo info@vetclinicpro.com
            </p>
            <p>
              Te esperamos y agradecemos tu confianza en nuestro equipo.
            </p>
          </div>
          <div class="footer">
            <p>Este es un mensaje automático, por favor no respondas directamente a este correo.</p>
            <p>VetClinic Pro · Centro Veterinario</p>
          </div>
        </div>
      </body>
    </html>
    """

    msg = MIMEText(body, "html", "utf-8")
    msg["Subject"] = subject
    msg["From"] = settings.SMTP_FROM
    msg["To"] = to_email

    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            if settings.SMTP_TLS:
                server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.sendmail(settings.SMTP_FROM, [to_email], msg.as_string())
    except Exception:
        # No interrumpir el flujo de la API por errores de envío de correo
        return


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
def create_appointment(appointment: AppointmentCreate, background_tasks: BackgroundTasks):
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

    # Intentar enviar correo de confirmación al dueño
    try:
        patient = patient_crud.get_by_id(appointment.pacienteId)
        if patient:
            to_email = patient.get("tutor_email") or patient.get("email")
            if to_email:
                background_tasks.add_task(send_appointment_email, to_email, new_appointment)
    except Exception:
        # No bloquear la creación de la cita si falla la obtención del paciente o el envío de correo
        pass

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
