from typing import List, Dict, Optional, Any
from database.firebase_client import get_firestore_client


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