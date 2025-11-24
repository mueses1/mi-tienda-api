from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class Product:
    """
    Modelo de dominio para productos.

    Representa un producto en la lógica de negocio y se mantiene
    independiente de FastAPI/Pydantic.
    """

    id: Optional[str]
    name: str
    price: float
    stock: int
    category: str
    image_url: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Product":
        """Crea un Product desde un dict (por ejemplo, documento Firestore)."""
        return cls(
            id=data.get("id"),
            name=data.get("name", ""),
            price=float(data.get("price", 0)),
            stock=int(data.get("stock", 0)),
            category=data.get("category", ""),
            image_url=data.get("image_url"),
        )

    def to_dict(self, include_id: bool = False) -> Dict[str, Any]:
        """
        Convierte el modelo a dict para guardar en Firestore u otra capa.

        Si include_id=True, incluye el campo "id" cuando exista.
        """
        data: Dict[str, Any] = {
            "name": self.name,
            "price": self.price,
            "stock": self.stock,
            "category": self.category,
            "image_url": self.image_url,
        }

        if include_id and self.id is not None:
            data["id"] = self.id

        return data