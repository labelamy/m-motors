from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import models, schemas, crud
from auth import create_access_token, get_current_user
from passlib.context import CryptContext
from typing import List
import os

router = APIRouter(prefix="/users", tags=["Users"])

# Context bcrypt pour les mots de passe hachés
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# -----------------------
# DB Session
# -----------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------------
# Authentification
# -----------------------
@router.post("/login", response_model=schemas.Token)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    """
    Login avec email et mot de passe.
    Retourne access_token si succès.
    """
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not pwd_context.verify(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")

    access_token = create_access_token({"sub": db_user.email, "role": db_user.role})
    return {"access_token": access_token, "token_type": "bearer"}

# -----------------------
# Inscription
# -----------------------
@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Crée un nouvel utilisateur.
    Hash automatiquement le mot de passe avec bcrypt.
    """
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        role="client"
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# -----------------------
# Liste des utilisateurs (admin uniquement)
# -----------------------
@router.get("/", response_model=List[schemas.UserResponse])
def list_users(db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Accès refusé, administrateur requis")
    return db.query(models.User).all()

# -----------------------
# Supprimer un utilisateur (admin uniquement)
# -----------------------
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Accès refusé")

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User non trouvé")

    db.delete(user)
    db.commit()
    return {"message": "User supprimé avec succès"}

# -----------------------
# Profil connecté
# -----------------------
@router.get("/me", response_model=schemas.UserResponse)
def get_me(current_user: schemas.UserResponse = Depends(get_current_user)):
    return current_user

# -----------------------
# Migration des anciens utilisateurs Render vers Supabase
# -----------------------
@router.post("/migrate")
def migrate_users(db: Session = Depends(get_db)):
    """
    Migrer les anciens utilisateurs Render vers Supabase.
    Remplacer RENDER_DB_URL par ton ancienne base.
    """
    from sqlalchemy import create_engine, text
    import os

    RENDER_DB_URL = os.getenv("RENDER_DB_URL")
    render_engine = create_engine(RENDER_DB_URL)
    render_session = Session(bind=render_engine.connect())

    old_users = render_session.execute(text("SELECT id, name, email, password, role, created_at FROM users")).fetchall()
    count = 0
    for u in old_users:
        exists = db.query(models.User).filter(models.User.email == u.email).first()
        if exists:
            continue
        db_user = models.User(
            id=u.id,
            name=u.name,
            email=u.email,
            password=u.password,  
            role=u.role,
            created_at=u.created_at
        )
        db.add(db_user)
        count += 1

    db.commit()
    render_session.close()
    return {"message": f"{count} utilisateurs migrés avec succès ✅"}

# Créer des utilisateurs de test

@router.post("/create-test-users")
def create_test_users(db: Session = Depends(get_db)):
    users_data = [
        {"name": "Admin", "email": "admin@test.com", "password": "1234", "role": "admin"},
        {"name": "Client1", "email": "client1@test.com", "password": "1234", "role": "client"},
        {"name": "Client2", "email": "client2@test.com", "password": "1234", "role": "client"},
    ]

    created = 0

    for u in users_data:
        # Vérifie si l'utilisateur existe déjà
        exists = db.query(models.User).filter(models.User.email == u["email"]).first()
        if exists:
            continue

        new_user = models.User(
            name=u["name"],
            email=u["email"],
            password=pwd_context.hash(u["password"]),
            role=u["role"]
        )

        db.add(new_user)
        created += 1

    db.commit()
    return {"message": f"{created} users créés ✅"}