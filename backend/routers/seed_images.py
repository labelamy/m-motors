# routers/seed_images.py
from fastapi import APIRouter
from pathlib import Path
import cloudinary.uploader
import os
from database import SessionLocal
import models

router = APIRouter()

def normalize_name(name: str) -> str:
    name = name.lower().replace(" ", "").replace("_", "").replace("-", "")

    # corrections intelligentes
    replacements = {
        "class": "classe",
        "c200": "cclass",
        "c220": "cclass",
        "c250": "cclass",
        "cx5": "cx5",  
    }

    for key, value in replacements.items():
        if key in name:
            return value

    return name

@router.get("/seed-images")
def seed_images():
    db = SessionLocal()
    BASE_DIR = Path(__file__).resolve().parent.parent
    images_dir = BASE_DIR / "seed_images"

    log = []

    for img_path in images_dir.glob("*.*"):
        filename = img_path.stem.lower()
        parts = filename.split("_")
        if len(parts) < 2:
            log.append(f"Ignoré (nom invalide) : {filename}")
            continue

        brand = parts[0].capitalize()
        model_file = " ".join(parts[1:]).capitalize()  # ex: model 3

        # Normalized pour matcher DB
        normalized_model_file = normalize_name(model_file)

        # Recherche dans la DB
        vehicules = db.query(models.Vehicule).filter(
            models.Vehicule.brand.ilike(brand)
        ).all()

        vehicule = None
        for v in vehicules:
            if normalize_name(v.model) == normalized_model_file or normalize_name(v.model) in normalized_model_file or normalized_model_file in normalize_name(v.model):
                vehicule = v
                log.append(f"DEBUG: fichier={normalized_model_file}")
                log.append(f"DEBUG: DB={normalize_name(v.model)}")
                break

        if not vehicule:
            log.append(f"Aucun véhicule trouvé pour {brand} {model_file}")
            continue

        if vehicule.image_url and vehicule.image_url.startswith("http"):
            log.append(f"{brand} {vehicule.model} déjà migré")
            continue

        try:
            result = cloudinary.uploader.upload(
                str(img_path),
                folder="vehicules_migration",
                overwrite=True,
                resource_type="image",
                transformation=[
                    {"width": 800, "height": 600, "crop": "limit", "quality": "auto"},
                    {"fetch_format": "auto"}
                ]
            )
            vehicule.image_url = result["secure_url"]
            db.commit()
            log.append(f"✔️ {brand} {vehicule.model} mis à jour → {result['secure_url']}")
        except Exception as e:
            log.append(f"Erreur pour {brand} {vehicule.model}: {str(e)}")
            db.rollback()

    db.close()
    return {"status": "Migration Cloudinary terminée ✅", "log": log}