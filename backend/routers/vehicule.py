from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, sessionmaker
from database import SessionLocal
import models, schemas
from auth import get_current_admin
from sqlalchemy import create_engine, text
import os
import crud

router = APIRouter(prefix="/vehicules", tags=["Vehicules"])

# -----------------------
# DB session
# -----------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------------
# CRUD existant
# -----------------------
@router.post("/", response_model=schemas.VehiculeResponse)
def create(
    vehicule: schemas.VehiculeCreate,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin)
):
    print(f"User connecté : {current_admin.email}, rôle : {current_admin.role}")
    return crud.create_vehicule(db, vehicule)

@router.get("/", response_model=list[schemas.VehiculeResponse])
def read_all(db: Session = Depends(get_db)):
    return crud.get_vehicules(db)

# -----------------------
# Migration Render → Supabase
# -----------------------
@router.post("/migrate")
def migrate_vehicules(db: Session = Depends(get_db)):
    """
    Migrer les véhicules de l'ancienne base Render vers Supabase.
    Accessible à l'admin seulement.
    """
    RENDER_DB_URL = os.getenv("RENDER_DB_URL")
    if not RENDER_DB_URL:
        raise HTTPException(status_code=500, detail="RENDER_DB_URL introuvable dans .env")

    # Connexion à la base Render
    render_engine = create_engine(RENDER_DB_URL)
    RenderSession = sessionmaker(bind=render_engine)
    render_db = RenderSession()

    try:
        # Extraction des véhicules
        old_vehicules = render_db.execute(text("""
            SELECT id, brand, model, year, price, kilometrage, carburant,
                   transmission, type, description, image_url, available, created_at
            FROM vehicules
        """)).fetchall()

        count = 0
        for v in old_vehicules:
            exists = db.query(models.Vehicule).filter(models.Vehicule.id == v.id).first()
            if exists:
                continue

            vehicule = models.Vehicule(
                id=v.id,
                brand=v.brand,
                model=v.model,
                year=v.year,
                price=v.price,
                kilometrage=v.kilometrage,
                carburant=v.carburant,
                transmission=v.transmission,
                type=v.type,
                description=v.description,
                image_url=v.image_url,
                available=v.available,
                created_at=v.created_at
            )
            db.add(vehicule)
            count += 1

        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur migration : {e}")
    finally:
        render_db.close()

    return {"message": f"{count} véhicules migrés avec succès ✅"}

@router.get("/{vehicule_id}", response_model=schemas.VehiculeResponse)
def get_one(vehicule_id: int, db: Session = Depends(get_db)):
    vehicule = db.query(models.Vehicule).filter(models.Vehicule.id == vehicule_id).first()

    if not vehicule:
        raise HTTPException(status_code=404, detail="Véhicule non trouvé")

    return vehicule