from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import SessionLocal
import backend.crud as crud
import backend.schemas as schemas
from backend.auth import create_access_token

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


# ========================
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