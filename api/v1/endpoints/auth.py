from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from crud.firebase_crud import FirebaseUserCRUD
import hashlib


router = APIRouter()

user_crud = FirebaseUserCRUD()


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    role: str
    name: str
    email: str


@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest):
    user = user_crud.get_by_email(request.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
        )

    # Validar contraseña
    stored_hash = user.get("password_hash")
    incoming_hash = hashlib.sha256(request.password.encode()).hexdigest()
    if not stored_hash or stored_hash != incoming_hash:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
        )

    # Token ficticio; aquí luego integrarás Firebase Auth / JWT real
    token = f"fake-token-for-{user['id']}"
    return LoginResponse(
        access_token=token,
        user_id=user["id"],
        role=user["role"],
        name=user["name"],
        email=user["email"],
    )