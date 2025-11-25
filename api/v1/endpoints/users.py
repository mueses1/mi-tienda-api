from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from schemas.user import UserInDB, UserCreate, UserUpdate
from crud.firebase_crud import FirebaseUserCRUD
from core.security import get_current_admin
import hashlib

router = APIRouter()

user_crud = FirebaseUserCRUD()


@router.get("/", response_model=List[UserInDB])
def get_all_users(current_admin = Depends(get_current_admin)):
    """Obtiene todos los usuarios usando modelos de dominio internamente.

    La respuesta sigue siendo una lista de UserInDB.
    """
    users = user_crud.get_all_models()
    # Convertir de modelo de dominio a dict compatible con UserInDB
    return [
        {
            "id": u.id,
            "email": u.email,
            "name": u.name,
            "role": u.role,
        }
        for u in users
        if u.id is not None
    ]


@router.get("/{user_id}", response_model=UserInDB)
def get_user(user_id: str, current_admin = Depends(get_current_admin)):
    """Obtiene un usuario por id usando el modelo de dominio internamente.

    Si no existe, devuelve 404 como antes.
    """
    user_model = user_crud.get_model_by_id(user_id)
    if not user_model or user_model.id is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {
        "id": user_model.id,
        "email": user_model.email,
        "name": user_model.name,
        "role": user_model.role,
    }


@router.post("/", response_model=UserInDB, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, current_admin = Depends(get_current_admin)):
    existing = user_crud.get_by_email(user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Ya existe un usuario con ese email")
    # Hashear contraseña antes de guardar
    password_hash = hashlib.sha256(user.password.encode()).hexdigest()
    data = user.model_dump(exclude={"password"})
    data["password_hash"] = password_hash
    new_user = user_crud.create(data)
    return new_user


@router.put("/{user_id}", response_model=UserInDB)
def update_user(user_id: str, user_update: UserUpdate, current_admin = Depends(get_current_admin)):
    update_data = user_update.model_dump(exclude_unset=True, exclude={"password"})
    # Si viene nueva contraseña, actualizar hash
    if user_update.password is not None:
        update_data["password_hash"] = hashlib.sha256(user_update.password.encode()).hexdigest()
    updated = user_crud.update(user_id, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return updated


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str, current_admin = Depends(get_current_admin)):
    deleted = user_crud.delete(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return None