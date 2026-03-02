from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
from auth import get_current_user, get_current_admin
import shutil
import os

router = APIRouter(prefix="/dossiers", tags=["Dossiers"])


@router.post("/")
def create_dossier(
    dossier: schemas.DossierCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    new_dossier = models.Dossier(
        user_id=current_user.id,
        vehicule_id=dossier.vehicule_id,
        type=dossier.type
    )
    db.add(new_dossier)
    db.commit()
    db.refresh(new_dossier)
    return new_dossier


@router.get("/me")
def get_my_dossiers(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return db.query(models.Dossier).filter(
        models.Dossier.user_id == current_user.id
    ).all()

@router.get("/admin", response_model=list[schemas.DossierResponse])
def get_all_dossiers(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")

    return db.query(models.Dossier).all()


@router.put("/admin/{dossier_id}/valider")
def validate_dossier(
    dossier_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403)

    dossier = db.query(models.Dossier).filter(
        models.Dossier.id == dossier_id
    ).first()

    dossier.status = "valide"
    db.commit()
    db.refresh(dossier)
    return {"message": "Dossier validé"}

UPLOAD_DIR = "uploads"
# Crée le dossier s'il n'existe pas
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

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

    dossier.document_path = file_path
    db.commit()
    db.refresh(dossier)

    return {"message": "Document uploadé avec succès"}

@router.put("/{dossier_id}/status")
def update_dossier_status(
    dossier_id: int,
    status: str,
    db: Session = Depends(get_db),
    admin: models.User = Depends(get_current_admin)
):
    dossier = db.query(models.Dossier).filter(
        models.Dossier.id == dossier_id
    ).first()

    if not dossier:
        raise HTTPException(status_code=404, detail="Dossier introuvable")

    if status not in ["accepte", "refuse"]:
        raise HTTPException(status_code=400, detail="Statut invalide")

    dossier.status = status
    db.commit()

    return {"message": f"Dossier {status}"}
