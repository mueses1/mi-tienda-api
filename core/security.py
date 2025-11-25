from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from crud.firebase_crud import FirebaseUserCRUD
from models.user import User


security = HTTPBearer()


def _extract_user_id_from_token(token: str) -> str:
    prefix = "fake-token-for-"
    if not token.startswith(prefix):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
        )
    return token[len(prefix) :]


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> User:
    """Obtiene el usuario actual a partir del token simple de autenticación.

    Por ahora se usa un token "fake-token-for-<user_id>". Más adelante
    se puede reemplazar por JWT u otra solución.
    """

    token = credentials.credentials
    user_id = _extract_user_id_from_token(token)

    crud = FirebaseUserCRUD()
    user_model = crud.get_model_by_id(user_id)
    if user_model is None or user_model.id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado para el token proporcionado",
        )

    return user_model


def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    """Dependencia que asegura que el usuario actual tenga rol admin."""

    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para realizar esta acción",
        )

    return current_user
