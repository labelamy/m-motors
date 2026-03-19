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
    BASE_DIR = Path(__file__).resolve().parent.parent  # backend/
    images_dir = BASE_DIR / "seed_images"

    log = []

    for img_path in images_dir.glob("*.*"):
        filename = img_path.stem.lower()  # ex: audi_a3
        parts = filename.split("_")
        if len(parts) < 2:
            log.append(f"Ignoré (nom invalide): {filename}")
            continue
        brand = parts[0].capitalize()
        model = parts[1].capitalize()

        vehicule = db.query(models.Vehicule).filter(
            models.Vehicule.brand.ilike(brand),
            models.Vehicule.model.ilike(model)
        ).first()

        if not vehicule:
            log.append(f"Aucun véhicule trouvé pour {brand} {model}")
            continue

        # Skip si déjà une URL Cloudinary
        if vehicule.image_url and vehicule.image_url.startswith("http"):
            log.append(f"{brand} {model} déjà migré")
            continue

        try:
            result = cloudinary.uploader.upload(
                str(img_path),
                folder="vehicules_migration"
            )
            vehicule.image_url = result["secure_url"]
            db.commit()
            log.append(f"✔️ {brand} {model} mis à jour")
        except Exception as e:
            log.append(f"Erreur pour {brand} {model}: {str(e)}")
            db.rollback()  # Ne pas perdre la session si erreur

    db.close()
    return {"status": "Migration Cloudinary terminée ✅", "log": log}