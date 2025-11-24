from fastapi import APIRouter, HTTPException, status
from typing import List
from schemas.user import UserInDB, UserCreate, UserUpdate
from crud.firebase_crud import FirebaseUserCRUD
import hashlib

router = APIRouter()

user_crud = FirebaseUserCRUD()


@router.get("/", response_model=List[UserInDB])
def get_all_users():
    return user_crud.get_all()


@router.get("/{user_id}", response_model=UserInDB)
def get_user(user_id: str):
    user = user_crud.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


@router.post("/", response_model=UserInDB, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
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
def update_user(user_id: str, user_update: UserUpdate):
    update_data = user_update.model_dump(exclude_unset=True, exclude={"password"})
    # Si viene nueva contraseña, actualizar hash
    if user_update.password is not None:
        update_data["password_hash"] = hashlib.sha256(user_update.password.encode()).hexdigest()
    updated = user_crud.update(user_id, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return updated


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str):
    deleted = user_crud.delete(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return None