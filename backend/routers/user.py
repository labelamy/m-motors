from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import crud 
import schemas 
from auth import create_access_token, get_current_user
from models import User
from typing import List


router = APIRouter()

# Gestion de la base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ========================
# Inscription
# ========================
@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Crée un nouvel utilisateur.
    Attends JSON : { email, password }
    """
    return crud.create_user(db, user)


# ===================================
# Login JSON compatible frontend
# ========================
@router.post("/login", response_model=schemas.Token)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    """
    Login compatible frontend.
    JSON attendu : { email, password }
    Retourne : { access_token, token_type }
    """
    db_user = crud.authenticate_user(db, user.email, user.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")

    access_token = create_access_token({"sub": db_user.email, "role": db_user.role})
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# ========================
# Delete user
# ========================
@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Supprimer un utilisateur (admin seulement)
    """

    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Accès refusé")

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return {"message": "User supprimé avec succès"}

# ==============================================
# GET /users - Liste de tous les utilisateurs
# ========================
@router.get("/users", response_model=List[schemas.UserResponse])
def list_users(
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """
    Retourne la liste de tous les utilisateurs.
    Accessible uniquement aux admins.
    """
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Accès refusé, administrateur requis")
    return crud.get_users(db)


# ==============================================
# GET /me - Profil de l'utilisateur connecté
# ========================
@router.get("/me", response_model=schemas.UserResponse)
def get_me(current_user: schemas.UserResponse = Depends(get_current_user)):
    """
    Retourne le profil de l'utilisateur connecté.
    """
    return current_user