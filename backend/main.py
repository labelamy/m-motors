from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text
from database import engine
import models
from routers import vehicule, user, dossiers
from logging_config import logger
from fastapi.staticfiles import StaticFiles

app = FastAPI()

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
    result = conn.execute(text("SELECT current_database();"))
    for row in result:
        print("FastAPI se connecte à la base :", row[0])

with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM vehicules;"))
    print("Véhicules dans la DB :", list(result))

# -----------------------
# Routes
# -----------------------
app.include_router(vehicule.router, prefix="/vehicules", tags=["Vehicules"])
app.include_router(user.router, prefix="/auth", tags=["Auth"])
app.include_router(dossiers.router)

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
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.mount("/images", StaticFiles(directory="images"), name="images")