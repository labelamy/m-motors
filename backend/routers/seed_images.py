from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pathlib import Path
import os
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
from database import SessionLocal
import models

# Charger les variables d'environnement
load_dotenv()

# Config Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

router = APIRouter()

@router.post("/seed-images")
def seed_images():
    db = SessionLocal()
    BASE_DIR = Path(__file__).resolve().parent.parent  # remonte au dossier backend
    images_dir = BASE_DIR / "seed_images"

    if not images_dir.exists():
        return JSONResponse({"error": "Le dossier seed_images est introuvable."}, status_code=404)

    count = 0
    for img_path in images_dir.glob("*.*"):
        try:
            filename = img_path.stem.lower()  # ex: audi_a3
            parts = filename.split("_")
            if len(parts) < 2:
                continue

            brand = parts[0].capitalize()
            model = parts[1].capitalize()

            # Cherche véhicule en DB
            vehicule = db.query(models.Vehicule).filter(
                models.Vehicule.brand.ilike(brand),
                models.Vehicule.model.ilike(model)
            ).first()

            if not vehicule:
                continue

            # Upload sur Cloudinary
            result = cloudinary.uploader.upload(
                str(img_path),
                folder="vehicules_migration"
            )
            vehicule.image_url = result["secure_url"]
            db.commit()
            count += 1

        except Exception as e:
            print(f"Erreur avec {img_path.name}: {e}")
            continue

    db.close()
    return {"status": f"Migration images terminée ✅ {count} images mises à jour."}