from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import schemas, crud
from auth import create_access_token
from logging_config import logger

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@router.post("/login", response_model=schemas.Token)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    
    logger.info(f"Tentative de connexion pour {user.email}")

    db_user = crud.authenticate_user(db, user.email, user.password)

    if not db_user:
        logger.warning(f"Echec connexion pour {user.email}")
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")

    logger.info(f"Connexion réussie pour {user.email}")

    token = create_access_token({"sub": db_user.email, "role": db_user.role})

    return {"access_token": token, "token_type": "bearer"}