from fastapi import APIRouter
from api.v1.endpoints import (
    products,
    users,
    auth,
    patients,
    appointments,
    settings,
    appointment_requests,
    cart,
)

api_router = APIRouter()
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(patients.router, prefix="/patients", tags=["patients"])
api_router.include_router(appointments.router, prefix="/appointments", tags=["appointments"])
api_router.include_router(settings.router, prefix="/settings", tags=["settings"])
api_router.include_router(
    appointment_requests.router,
    prefix="/appointment-requests",
    tags=["appointment-requests"],
)
api_router.include_router(cart.router, prefix="/cart", tags=["cart"])