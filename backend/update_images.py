# update_images_cloudinary.py
from dotenv import load_dotenv
import os
from pathlib import Path
import cloudinary
import cloudinary.uploader
from database import SessionLocal
import models

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

db = SessionLocal()
BASE_DIR = Path(__file__).resolve().parent
images_dir = BASE_DIR / "seed_images"

def normalize_name(name: str) -> str:
    return name.replace(" ", "").replace("_", "").lower()

for img_path in images_dir.glob("*.*"):
    try:
        filename = img_path.stem.lower()
        print(f"Traitement : {filename}")

        parts = filename.split("_")
        if len(parts) < 2:
            print(f"Ignoré (format invalide) : {filename}")
            continue

        brand = parts[0].capitalize()
        model_file = " ".join(parts[1:]).capitalize()
        normalized_model_file = normalize_name(model_file)

        vehicules = db.query(models.Vehicule).filter(
            models.Vehicule.brand.ilike(brand)
        ).all()

        vehicule = None
        for v in vehicules:
            if normalize_name(v.model) == normalized_model_file:
                vehicule = v
                break

        if not vehicule:
            print(f"Aucun véhicule trouvé pour {brand} {model_file}")
            continue

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
        print(f"✔️ {brand} {vehicule.model} mis à jour → {result['secure_url']}")

    except Exception as e:
        print(f"Erreur pour {filename}: {e}")

db.close()
print("✅ Migration Cloudinary terminée !")