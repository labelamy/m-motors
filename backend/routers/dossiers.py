from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db
import models 
import schemas 
from auth import get_current_user, get_current_admin
import shutil
import os

router = APIRouter(prefix="/dossiers", tags=["Dossiers"])

UPLOAD_DIR = "uploads"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


# 🔹 Créer dossier
@router.post("/")
def create_dossier(
    dossier: schemas.DossierCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    
     # Vérifier si le véhicule existe
    vehicule = db.query(models.Vehicule).filter(
        models.Vehicule.id == dossier.vehicule_id
    ).first()

    if not vehicule:
        raise HTTPException(status_code=404, detail="Véhicule introuvable")

    # Vérifier si le véhicule est disponible
    if not vehicule.available:
        raise HTTPException(status_code=400, detail="Ce véhicule est déjà réservé")

     # Vérifier si un dossier existe déjà pour ce véhicule
    existing = db.query(models.Dossier).filter(
        models.Dossier.user_id == current_user.id,
        models.Dossier.vehicule_id == dossier.vehicule_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Un dossier existe déjà pour ce véhicule"
        )
     # 📁 Création du dossier
    new_dossier = models.Dossier(
        user_id=current_user.id,
        vehicule_id=dossier.vehicule_id,
        type=dossier.type,
        status="EN_ATTENTE"
    )

    db.add(new_dossier)
    db.commit()
    db.refresh(new_dossier)

    return new_dossier


# 🔹 Voir ses dossiers
@router.get("/mes-dossiers", response_model=list[schemas.DossierResponse])
def get_my_dossiers(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return db.query(models.Dossier).filter(
        models.Dossier.user_id == current_user.id
    ).all()


# 🔹 Voir tous les dossiers (admin)
@router.get("/admin", response_model=list[schemas.DossierResponse])
def get_all_dossiers(
    db: Session = Depends(get_db),
    admin: models.User = Depends(get_current_admin)
):
    return db.query(models.Dossier).all()


# 🔹 Upload document
@router.post("/{dossier_id}/upload")
def upload_document(
    dossier_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    dossier = db.query(models.Dossier).filter(
        models.Dossier.id == dossier_id,
        models.Dossier.user_id == current_user.id
    ).first()

    if not dossier:
        raise HTTPException(status_code=404, detail="Dossier non trouvé")

    file_path = os.path.join(UPLOAD_DIR, f"{dossier_id}_{file.filename}")

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    dossier.document_path = f"/uploads/{dossier_id}_{file.filename}"

    db.commit()
    db.refresh(dossier)

    return {"message": "Document uploadé avec succès"}


# 🔹 Valider dossier (admin)
@router.put("/{dossier_id}/validate")
def validate_dossier(
    dossier_id: int,
    db: Session = Depends(get_db),
    admin: models.User = Depends(get_current_admin)
):

    dossier = db.query(models.Dossier).filter(
        models.Dossier.id == dossier_id
    ).first()

    if not dossier:
        raise HTTPException(status_code=404, detail="Dossier introuvable")

    dossier.status = "VALIDE"
    db.commit()

    return {"message": "Dossier validé"}


# 🔹 Refuser dossier (admin)
@router.put("/{dossier_id}/refuse")
def refuse_dossier(
    dossier_id: int,
    db: Session = Depends(get_db),
    admin: models.User = Depends(get_current_admin)
):

    dossier = db.query(models.Dossier).filter(
        models.Dossier.id == dossier_id
    ).first()

    if not dossier:
        raise HTTPException(status_code=404, detail="Dossier introuvable")

    dossier.status = "REFUSE"
    db.commit()

    return {"message": "Dossier refusé"}