from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class User:
    """
    Modelo de dominio para usuarios.

    Independiente de FastAPI/Pydantic. Útil para lógica de negocio,
    permisos, etc.
    """

    id: Optional[str]
    email: str
    name: str
    role: str  # ej: "admin", "customer"
    hashed_password: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "User":
        """Crea un User desde un dict (documento Firestore)."""
        return cls(
            id=data.get("id"),
            email=data.get("email", ""),
            name=data.get("name", ""),
            role=data.get("role", ""),
            hashed_password=data.get("hashed_password"),
        )

    def to_dict(self, include_id: bool = False) -> Dict[str, Any]:
        """
        Convierte el modelo a dict para guardar en Firestore u otra capa.

        Si include_id=True, incluye el campo "id" cuando exista.
        """
        data: Dict[str, Any] = {
            "email": self.email,
            "name": self.name,
            "role": self.role,
            "hashed_password": self.hashed_password,
        }

        if include_id and self.id is not None:
            data["id"] = self.id

        return data