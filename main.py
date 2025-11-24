from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from api.v1.api import api_router
from core.config import settings

app = FastAPI(
    title="Mi Tienda API - Desacoplamiento Monolito",
    description="API RESTful para el proyecto final - Corte 3",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url="/docs",      # Swagger UI
    redoc_url="/redoc"
)

# CORS para frontend en localhost (React/Vite)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React clásico
        "http://localhost:5173",  # Vite
    ],  # Cambiar en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

# Archivos estáticos (imágenes de productos, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return {"message": "API de Mi Tienda - Backend desacoplado con FastAPI"}