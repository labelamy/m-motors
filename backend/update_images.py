# update_images_cloudinary.py
from dotenv import load_dotenv
import os
from pathlib import Path
import cloudinary
import cloudinary.uploader
from database import SessionLocal
import models

# Charger les variables d'environnement depuis .env
load_dotenv()

# Config Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

# Connexion à la DB
db = SessionLocal()

# Dossier contenant les images à migrer
BASE_DIR = Path(__file__).resolve().parent
images_dir = BASE_DIR / "seed_images"

for img_path in images_dir.glob("*.*"):
    try:
        filename = img_path.stem.lower()  # ex: audi_a3
        print(f"Traitement: {filename}")

        # On suppose format: brand_model.jpg
        parts = filename.split("_")
        if len(parts) < 2:
            print(f"Nom ignoré (format invalide) : {filename}")
            continue

        brand = parts[0].capitalize()
        model = "_".join(parts[1:]).capitalize()  # supporte des noms composés

        # Cherche véhicule en DB
        vehicule = db.query(models.Vehicule).filter(
            models.Vehicule.brand.ilike(brand),
            models.Vehicule.model.ilike(model)
        ).first()

        if not vehicule:
            print(f"Aucun véhicule trouvé pour {brand} {model}")
            continue

        # Upload sur Cloudinary
        result = cloudinary.uploader.upload(
            str(img_path),
            folder="vehicules_migration",
            overwrite=True,
            resource_type="image"
        )

        # Mettre à jour le véhicule avec l'URL publique
        vehicule.image_url = result["secure_url"]
        db.commit()

        print(f"✔️ {brand} {model} mis à jour → {result['secure_url']}")

    except Exception as e:
        print(f"Erreur pour {filename}: {e}")

db.close()
print("✅ Migration Cloudinary terminée !")