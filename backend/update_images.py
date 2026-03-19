from dotenv import load_dotenv
import os
from pathlib import Path

# Charger .env
# Chemin explicite vers .env
BASE_DIR = Path(__file__).resolve().parent
env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path)

print("DATABASE_URL =", os.getenv("DATABASE_URL"))

import cloudinary
import cloudinary.uploader
from pathlib import Path
from database import SessionLocal
import models




# Config Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

# Connexion DB
db = SessionLocal()

# Dossier images
BASE_DIR = Path(__file__).resolve().parent
images_dir = BASE_DIR / "seed_images"

# Parcours des images
for img_path in images_dir.glob("*.*"):
    try:
        filename = img_path.stem.lower()  # ex: mini_cooper

        print(f"Traitement: {filename}")

        # On suppose format: brand_model.jpg
        parts = filename.split("_")
        if len(parts) < 2:
            print(f"Nom ignoré: {filename}")
            continue

        brand = parts[0].capitalize()
        model = parts[1].capitalize()

        # Cherche véhicule en DB
        vehicule = db.query(models.Vehicule).filter(
            models.Vehicule.brand.ilike(brand),
            models.Vehicule.model.ilike(model)
        ).first()

        if not vehicule:
            print(f"Aucun véhicule trouvé pour {brand} {model}")
            continue

        # Upload Cloudinary
        result = cloudinary.uploader.upload(
            str(img_path),
            folder="vehicules_migration"
        )

        image_url = result["secure_url"]

        # Mise à jour DB
        vehicule.image_url = image_url
        db.commit()

        print(f"✔️ {brand} {model} mis à jour")

    except Exception as e:
        print(f"Erreur: {e}")

db.close()
print("✅ Migration terminée !")