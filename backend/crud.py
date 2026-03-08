from fastapi  import HTTPException

from sqlalchemy.orm import Session
import backend.models as models
import backend.schemas as schemas
from backend.auth import hash_password, verify_password

# VEHICULES
# -----------------------------

def create_vehicule(db: Session, vehicule: schemas.VehiculeCreate):
    db_vehicule = models.Vehicule(**vehicule.model_dump())
    db.add(db_vehicule)
    db.commit()
    db.refresh(db_vehicule)
    return db_vehicule

def get_vehicules(db: Session):
    return db.query(models.Vehicule).all()

# USERS
# -----------------------------

def create_user(db: Session, user: schemas.UserCreate):
    existing_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email déjà utilisé")

    hashed_pwd = hash_password(user.password)
    db_user = models.User(email=user.email, password=hashed_pwd)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user

# REHASH DES MOTS DE PASSE EXISTANTS
# -----------------------------
def rehash_existing_users(db: Session):
    """
    Vérifie tous les utilisateurs existants et rehash les mots de passe
    qui ne sont pas encore en bcrypt.
    """
    users = db.query(models.User).all()
    for user in users:
        if not user.password.startswith("$2b$"):  # bcrypt hash commence par $2b$
            user.password = hash_password(user.password)
    db.commit()