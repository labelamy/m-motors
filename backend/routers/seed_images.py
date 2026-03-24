from fastapi import APIRouter
from pathlib import Path
import cloudinary.uploader
from database import SessionLocal
import models

router = APIRouter()


def normalize_name(name: str) -> str:
    name = name.lower().replace(" ", "").replace("_", "").replace("-", "")

    # cas spécifiques (AVANT toute logique générale)
    if any(x in name for x in ["cclass", "c200", "c220", "c250"]):
        return "cclass"

    if any(x in name for x in ["classea", "aclass"]):
        return "classea"

    if "cx5" in name:
        return "cx5"

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

        brand = parts[0]  # ❌ pas de capitalize
        model_file = "".join(parts[1:])  # plus simple et fiable

        normalized_model_file = normalize_name(model_file)

        vehicules = db.query(models.Vehicule).filter(
            models.Vehicule.brand.ilike(brand)
        ).all()

        vehicule = None

        for v in vehicules:
            db_model = normalize_name(v.model)

            log.append(f"[TEST] file={normalized_model_file} | db={db_model}")

            if db_model == normalized_model_file:
                vehicule = v
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

            log.append(f"✔️ {brand} {vehicule.model} mis à jour")

        except Exception as e:
            db.rollback()
            log.append(f"❌ Erreur pour {brand} {model_file}: {str(e)}")

    db.close()

    return {
        "status": "Migration Cloudinary terminée ✅",
        "log": log
    }