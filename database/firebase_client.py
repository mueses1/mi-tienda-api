import firebase_admin
from firebase_admin import credentials, firestore
from core.config import settings

# Singleton de Firestore
_firestore_client = None


def get_firestore_client():
    global _firestore_client
    if _firestore_client is not None:
        return _firestore_client

    if not firebase_admin._apps:
        if not settings.FIREBASE_CREDENTIALS_PATH:
            raise RuntimeError("FIREBASE_CREDENTIALS_PATH no está configurado")

        cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
        firebase_admin.initialize_app(cred, {
        })

    _firestore_client = firestore.client()
    return _firestore_client