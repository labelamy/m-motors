from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text
from backend.database import engine
import backend.models as models
from backend.routers import vehicule, user, dossiers
from backend.logging_config import logger
from fastapi.staticfiles import StaticFiles
from pathlib import Path 
from backend.routers import auth

app = FastAPI(title="Motors API", description="API pour la gestion des véhicules et dossiers de réparation", version="1.0.0")

# -----------------------
# CORS pour frontend React
# -----------------------
origins = [
    "http://localhost:5173",  # ton frontend
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
# models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

with engine.connect() as conn:
    result = conn.execute(text("SELECT 1"))
    print("Connexion à la DB OK :", list(result))

# -----------------------
# Routes
# -----------------------
app.include_router(vehicule.router, prefix="/vehicules", tags=["Vehicules"])
app.include_router(user.router, prefix="/auth", tags=["Auth"])
app.include_router(dossiers.router)
#app.include_router(auth.router)

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