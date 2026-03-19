# routers/seed_images.py
from fastapi import APIRouter
from pathlib import Path
import cloudinary.uploader
import os
from database import SessionLocal
import models

router = APIRouter()

@router.get("/seed-images")
def seed_images():
    db = SessionLocal()
    BASE_DIR = Path(__file__).resolve().parent.parent  # remonte à backend/
    images_dir = BASE_DIR / "seed_images"

    for img_path in images_dir.glob("*.*"):
        filename = img_path.stem.lower()  # ex: audi_a3
        parts = filename.split("_")
        if len(parts) < 2:
            continue
        brand = parts[0].capitalize()
        model = parts[1].capitalize()

        vehicule = db.query(models.Vehicule).filter(
            models.Vehicule.brand.ilike(brand),
            models.Vehicule.model.ilike(model)
        ).first()

        if not vehicule:
            continue

        try:
            result = cloudinary.uploader.upload(
                str(img_path),
                folder="vehicules_migration"
            )
            vehicule.image_url = result["secure_url"]
            db.commit()
        except Exception as e:
            return {"error": f"Erreur pour {filename}: {str(e)}"}

    db.close()
    return {"status": "Migration Cloudinary terminée ✅"}