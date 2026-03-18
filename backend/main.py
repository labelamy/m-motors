from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text
from database import engine
import models
from routers import vehicule, user, dossiers ,auth
from logging_config import logger
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI(
    title="Motors API",
    description="API pour la gestion des véhicules et dossiers de réparation",
    version="1.0.0"
)

# -----------------------
# CORS pour frontend React
# -----------------------
origins = [
    "http://localhost:5173",
    "https://m-motors.vercel.app"  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------
# Création tables + test DB
# -----------------------
models.Base.metadata.create_all(bind=engine)

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT current_database();"))
        print("FastAPI se connecte à la base :", list(result))
except Exception as e:
    print("Erreur connexion DB :", e)

# Test simple pour éviter le crash si table vide
try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("Connexion DB OK :", list(result))
except Exception as e:
    print("Erreur test DB :", e)

# -----------------------
# Routes
# -----------------------
app.include_router(vehicule.router, prefix="/vehicules", tags=["Vehicules"])
app.include_router(user.router, prefix="/auth", tags=["Auth"])
app.include_router(dossiers.router)
app.include_router(auth.router)
# app.include_router(auth.router)  # décommente si nécessaire

@app.get("/")
def root():
    return {"message": "API M-Motors opérationnelle 🚗"}

# -----------------------
# Logging global des erreurs
# -----------------------
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Erreur serveur: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Erreur interne du serveur"}
    )

# --------------------------------------------------------------
# Servir les fichiers statiques (images de véhicules & uploads)
# --------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent

(BASE_DIR / "uploads").mkdir(exist_ok=True)
(BASE_DIR / "images").mkdir(exist_ok=True)

app.mount("/uploads", StaticFiles(directory=BASE_DIR / "uploads"), name="uploads")
app.mount("/images", StaticFiles(directory=BASE_DIR / "images"), name="images")