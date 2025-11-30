from typing import List, Dict, Optional, Any
from database.firebase_client import get_firestore_client
from models.product import Product
from models.user import User

class FirebaseProductCRUD:
    def __init__(self):
        self._db = get_firestore_client()
        self._collection = self._db.collection("products")

    def get_all(self) -> List[dict]:
        docs = self._collection.stream()
        return [{**d.to_dict(), "id": d.id} for d in docs]

    def get_by_id(self, product_id: str) -> Optional[dict]:
        doc = self._collection.document(product_id).get()
        if not doc.exists:
            return None
        return {**doc.to_dict(), "id": doc.id}

    def create(self, data: Dict[str, Any]) -> dict:
        doc_ref = self._collection.document()  # id automático
        doc_ref.set(data)
        return {**data, "id": doc_ref.id}

    def update(self, product_id: str, data: Dict[str, Any]) -> Optional[dict]:
        doc_ref = self._collection.document(product_id)
        if not doc_ref.get().exists:
            return None
        doc_ref.update(data)
        updated = doc_ref.get().to_dict()
        return {**updated, "id": product_id}

    def delete(self, product_id: str) -> bool:
        doc_ref = self._collection.document(product_id)
        if not doc_ref.get().exists:
            return False
        doc_ref.delete()
        return True

    # --- Helpers de modelos de dominio ---

    def get_all_models(self) -> List[Product]:
        """Obtiene todos los productos como modelos de dominio Product."""
        data_list = self.get_all()
        return [Product.from_dict(data) for data in data_list]

    def get_model_by_id(self, product_id: str) -> Optional[Product]:
        """Obtiene un producto como Product o None si no existe."""
        data = self.get_by_id(product_id)
        if data is None:
            return None
        return Product.from_dict(data)

    def create_model(self, product: Product) -> Product:
        """Crea un producto a partir de un modelo de dominio y devuelve el modelo creado."""
        created_data = self.create(product.to_dict())
        return Product.from_dict(created_data)

    def update_model(self, product_id: str, product: Product) -> Optional[Product]:
        """Actualiza un producto usando un modelo de dominio y devuelve el modelo actualizado."""
        updated_data = self.update(product_id, product.to_dict())
        if updated_data is None:
            return None
        return Product.from_dict(updated_data)


class FirebaseUserCRUD:
    def __init__(self):
        self._db = get_firestore_client()
        self._collection = self._db.collection("users")

    def get_all(self) -> List[dict]:
        docs = self._collection.stream()
        return [{**d.to_dict(), "id": d.id} for d in docs]

    def get_by_id(self, user_id: str) -> Optional[dict]:
        doc = self._collection.document(user_id).get()
        if not doc.exists:
            return None
        return {**doc.to_dict(), "id": doc.id}

    def get_by_email(self, email: str) -> Optional[dict]:
        docs = self._collection.where("email", "==", email).limit(1).stream()
        for d in docs:
            return {**d.to_dict(), "id": d.id}
        return None

    def create(self, data: Dict[str, Any]) -> dict:
        doc_ref = self._collection.document()
        doc_ref.set(data)
        return {**data, "id": doc_ref.id}

    def update(self, user_id: str, data: Dict[str, Any]) -> Optional[dict]:
        doc_ref = self._collection.document(user_id)
        if not doc_ref.get().exists:
            return None
        doc_ref.update(data)
        updated = doc_ref.get().to_dict()
        return {**updated, "id": user_id}

    def delete(self, user_id: str) -> bool:
        doc_ref = self._collection.document(user_id)
        if not doc_ref.get().exists:
            return False
        doc_ref.delete()
        return True

    # --- Helpers de modelos de dominio ---

    def get_all_models(self) -> List[User]:
        """Obtiene todos los usuarios como modelos de dominio User."""
        data_list = self.get_all()
        users: List[User] = []
        for data in data_list:
            # Mapear password_hash almacenado a hashed_password del dominio
            mapped = {
                **data,
                "hashed_password": data.get("password_hash"),
            }
            users.append(User.from_dict(mapped))
        return users

    def get_model_by_id(self, user_id: str) -> Optional[User]:
        """Obtiene un usuario como User o None si no existe."""
        data = self.get_by_id(user_id)
        if data is None:
            return None
        mapped = {**data, "hashed_password": data.get("password_hash")}
        return User.from_dict(mapped)

    def create_model(self, user: User) -> User:
        """Crea un usuario a partir de un modelo de dominio y devuelve el modelo creado.

        Nota: se espera que User.hashed_password ya contenga el hash.
        """
        data: Dict[str, Any] = user.to_dict(include_id=False)
        # Renombrar hashed_password -> password_hash para almacenamiento
        if "hashed_password" in data:
            data["password_hash"] = data.pop("hashed_password")
        created = self.create(data)
        mapped = {**created, "hashed_password": created.get("password_hash")}
        return User.from_dict(mapped)

    def update_model(self, user_id: str, user: User) -> Optional[User]:
        """Actualiza un usuario usando un modelo de dominio y devuelve el modelo actualizado."""
        data: Dict[str, Any] = user.to_dict(include_id=False)
        if "hashed_password" in data:
            data["password_hash"] = data.pop("hashed_password")
        updated = self.update(user_id, data)
        if updated is None:
            return None
        mapped = {**updated, "hashed_password": updated.get("password_hash")}
        return User.from_dict(mapped)


class FirebasePatientCRUD:
    def __init__(self):
        self._db = get_firestore_client()
        self._collection = self._db.collection("patients")

    def get_all(self) -> List[dict]:
        docs = self._collection.stream()
        return [{**d.to_dict(), "id": d.id} for d in docs]

    def get_by_id(self, patient_id: str) -> Optional[dict]:
        doc = self._collection.document(patient_id).get()
        if not doc.exists:
            return None
        return {**doc.to_dict(), "id": doc.id}

    def create(self, data: Dict[str, Any]) -> dict:
        doc_ref = self._collection.document()
        doc_ref.set(data)
        return {**data, "id": doc_ref.id}

    def update(self, patient_id: str, data: Dict[str, Any]) -> Optional[dict]:
        doc_ref = self._collection.document(patient_id)
        if not doc_ref.get().exists:
            return None
        doc_ref.update(data)
        updated = doc_ref.get().to_dict()
        return {**updated, "id": patient_id}

    def delete(self, patient_id: str) -> bool:
        doc_ref = self._collection.document(patient_id)
        if not doc_ref.get().exists:
            return False
        doc_ref.delete()
        return True


class FirebaseAppointmentCRUD:
    def __init__(self):
        self._db = get_firestore_client()
        self._collection = self._db.collection("appointments")

    def get_all(self) -> List[dict]:
        docs = self._collection.stream()
        return [{**d.to_dict(), "id": d.id} for d in docs]

    def get_by_id(self, appointment_id: str) -> Optional[dict]:
        doc = self._collection.document(appointment_id).get()
        if not doc.exists:
            return None
        return {**doc.to_dict(), "id": doc.id}

    def create(self, data: Dict[str, Any]) -> dict:
        doc_ref = self._collection.document()
        doc_ref.set(data)
        return {**data, "id": doc_ref.id}

    def update(self, appointment_id: str, data: Dict[str, Any]) -> Optional[dict]:
        doc_ref = self._collection.document(appointment_id)
        if not doc_ref.get().exists:
            return None
        doc_ref.update(data)
        updated = doc_ref.get().to_dict()
        return {**updated, "id": appointment_id}

    def delete(self, appointment_id: str) -> bool:
        doc_ref = self._collection.document(appointment_id)
        if not doc_ref.get().exists:
            return False
        doc_ref.delete()
        return True


class FirebaseAppointmentRequestCRUD:
    def __init__(self):
        self._db = get_firestore_client()
        self._collection = self._db.collection("appointment_requests")

    def get_all(self) -> List[dict]:
        docs = self._collection.stream()
        return [{**d.to_dict(), "id": d.id} for d in docs]

    def get_by_id(self, request_id: str) -> Optional[dict]:
        doc = self._collection.document(request_id).get()
        if not doc.exists:
            return None
        return {**doc.to_dict(), "id": doc.id}

    def create(self, data: Dict[str, Any]) -> dict:
        doc_ref = self._collection.document()
        doc_ref.set(data)
        return {**data, "id": doc_ref.id}

    def update(self, request_id: str, data: Dict[str, Any]) -> Optional[dict]:
        doc_ref = self._collection.document(request_id)
        if not doc_ref.get().exists:
            return None
        doc_ref.update(data)
        updated = doc_ref.get().to_dict()
        return {**updated, "id": request_id}

    def delete(self, request_id: str) -> bool:
        doc_ref = self._collection.document(request_id)
        if not doc_ref.get().exists:
            return False
        doc_ref.delete()
        return True


class FirebaseSettingsCRUD:
    def __init__(self):
        self._db = get_firestore_client()
        self._collection = self._db.collection("settings")
        self._doc_id = "global-config"

    def get(self) -> Optional[dict]:
        doc = self._collection.document(self._doc_id).get()
        if not doc.exists:
            return None
        return doc.to_dict()

    def upsert(self, data: Dict[str, Any]) -> dict:
        doc_ref = self._collection.document(self._doc_id)
        # merge=True para actualizar solo las secciones enviadas
        doc_ref.set(data, merge=True)
        saved = doc_ref.get().to_dict() or {}
        return saved


class FirebaseCartCRUD:
    def __init__(self):
        self._db = get_firestore_client()
        self._collection = self._db.collection("carts")

    def get_cart(self, user_id: str) -> Optional[dict]:
        doc = self._collection.document(user_id).get()
        if not doc.exists:
            return {"user_id": user_id, "items": []}
        data = doc.to_dict() or {}
        data.setdefault("user_id", user_id)
        data.setdefault("items", [])
        return data

    def add_or_update_item(self, user_id: str, item: Dict[str, Any]) -> dict:
        cart: Dict[str, Any] = self.get_cart(user_id)
        items: List[Dict[str, Any]] = cart.get("items", [])
        product_id = item.get("product_id")
        if not product_id:
            raise ValueError("product_id es requerido para el item del carrito")

        updated = False
        for existing in items:
            if existing.get("product_id") == product_id:
                quantity = existing.get("quantity", 1) + item.get("quantity", 1)
                existing.update({**item, "quantity": quantity})
                updated = True
                break
        if not updated:
            if "quantity" not in item:
                item["quantity"] = 1
            items.append(item)
        self._collection.document(user_id).set({"items": items}, merge=True)
        return {"user_id": user_id, "items": items}

    def remove_item(self, user_id: str, product_id: str) -> dict:
        cart = self.get_cart(user_id)
        items = cart.get("items", [])
        items = [i for i in items if i.get("product_id") != product_id]
        self._collection.document(user_id).set({"items": items}, merge=True)
        return {"user_id": user_id, "items": items}

    def clear_cart(self, user_id: str) -> dict:
        self._collection.document(user_id).set({"items": []}, merge=True)
        return {"user_id": user_id, "items": []}


class FirebaseOrderCRUD:
    def __init__(self):
        self._db = get_firestore_client()
        self._collection = self._db.collection("orders")

    def create(self, data: Dict[str, Any]) -> dict:
        doc_ref = self._collection.document()
        doc_ref.set(data)
        return {**data, "id": doc_ref.id}

    def get_by_id(self, order_id: str) -> Optional[dict]:
        doc = self._collection.document(order_id).get()
        if not doc.exists:
            return None
        return {**doc.to_dict(), "id": doc.id}

    def get_all_by_user(self, user_id: str) -> List[dict]:
        docs = self._collection.where("user_id", "==", user_id).stream()
        return [{**d.to_dict(), "id": d.id} for d in docs]