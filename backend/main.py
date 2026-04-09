from fastapi import FastAPI, Request, APIRouter, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text
from database import engine, SessionLocal
import models
from routers import vehicule, user, dossiers, auth, seed_images
from logging_config import logger
from pathlib import Path
import os
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
import random
from sqlalchemy.orm import Session

# -----------------------
# Load env + config Cloudinary
# -----------------------
load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

# -----------------------
# App FastAPI
# -----------------------
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

# Test simple
try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("Connexion DB OK :", list(result))
except Exception as e:
    print("Erreur test DB :", e)

# -----------------------
# Routes existantes
# -----------------------
app.include_router(vehicule.router)
app.include_router(user.router)
app.include_router(dossiers.router)
app.include_router(auth.router)
# Router temporaire pour migration
app.include_router(seed_images.router)

@app.get("/")
def root():
    return {"message": "API M-Motors opérationnelle 🚗"}

# -----------------------
# Logging global
# -----------------------
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Erreur serveur: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Erreur interne du serveur"}
    )

# -----------------------
# Endpoint upload Cloudinary
# -----------------------
upload_router = APIRouter()

@upload_router.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    try:
        result = cloudinary.uploader.upload(file.file, folder="vehicules")
        return JSONResponse({"url": result["secure_url"]})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

app.include_router(upload_router)

# -----------------------
# Endpoint /seed pour remplir la DB avec véhicules et images Cloudinary
# -----------------------
seed_router = APIRouter()

@seed_router.post("/seed")
def seed_db():
    db: Session = SessionLocal()
    try:
        brands = ["Lexus", "Maserati", "Mitsubishi", "Citroen", "Chrysler", "Lamborghini", "Ferrari", "Porsche", "Opel", "Gmc"]
        models_list = ["A", "B", "C", "X", "Y"]
        carburants = ["Essence", "Diesel", "Electrique", "Hybride"]
        transmissions = ["Manuelle", "Automatique"]
        vehicule_images = {
            ("Lexus", "A"): "https://res.cloudinary.com/dwb8kogm4/image/upload/v1775744091/lexus_a_qmh8vk.jpg",
            ("Lamborghini", "Y"): "https://res.cloudinary.com/dwb8kogm4/image/upload/v1775744072/lamborghini_y_nthb7w.jpg",
            ("Citroen", "B"): "https://res.cloudinary.com/dwb8kogm4/image/upload/v1775743951/citroen_b_nbaiwd.jpg",
            ("Citroen", "C"): "https://res.cloudinary.com/dwb8kogm4/image/upload/v1775743969/citroen_c_uyc1qk.jpg",
            ("Lamborghini", "A"): "https://res.cloudinary.com/dwb8kogm4/image/upload/v1775744057/lamborghini_a_qh3h7p.jpg",
            ("Ferrari", "C"): "https://res.cloudinary.com/dwb8kogm4/image/upload/v1775743765/ferrari_c_m0s3cz.jpg",
            ("Porsche", "X"): "https://res.cloudinary.com/dwb8kogm4/image/upload/v1775744131/porsche_x_a6v1fk.jpg",
            ("Ferrari", "Y"): "https://res.cloudinary.com/dwb8kogm4/image/upload/v1775744013/ferrari_y_njiltt.jpg",
            ("Gmc", "Y"): "https://res.cloudinary.com/dwb8kogm4/image/upload/v1775744036/gmc_y_somm23.jpg",
        }
        images_sample = [
            "https://res.cloudinary.com/demo/image/upload/sample.jpg",
            "https://res.cloudinary.com/demo/image/upload/sample.jpg"
        ]

        # Supprime les véhicules existants
        db.query(models.Vehicule).delete()
        db.commit()

        # Chemin vers les images locales de test
        BASE_DIR = Path(__file__).resolve().parent
        images_dir = BASE_DIR / "seed_images"
        images_paths = list(images_dir.glob("*.jpg"))

        if not images_paths:
            return {"error": "Aucune image trouvée dans seed_images !"}

        # Crée 10 véhicules de test
        for i in range(10):
            vehicule = models.Vehicule(
                brand=random.choice(brands),
                model=random.choice(models_list),
                year=random.randint(2015, 2023),
                price=round(random.uniform(10000, 50000), 2),
                kilometrage=random.randint(0, 150000),
                carburant=random.choice(carburants),
                transmission=random.choice(transmissions),
                type=random.choice(["achat", "location"]),
                description=f"Description du véhicule {i+1}",
                image_url=vehicule_images.get((brands, models), "https://res.cloudinary.com/dwb8kogm4/image/upload/v1775748900/default_car_cbffel.png"),
                available=True
            )
            db.add(vehicule)
        db.commit()
        return {"message": "DB remplie avec succès !"}
    except Exception as e:
        db.rollback()
        return JSONResponse({"error": str(e)}, status_code=500)
    finally:
        db.close()

app.include_router(seed_router)