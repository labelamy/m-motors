from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

import backend.schemas as schemas
import backend.crud as crud
from backend.database import get_db
from backend.auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, verify_password

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

# REGISTER
# ------------------------

@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Crée un nouvel utilisateur avec mot de passe hashé.
    """
    db_user = crud.create_user(db, user)
    return db_user

# LOGIN
# ------------------------

@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Authentifie l'utilisateur et retourne un JWT.
    Utilise OAuth2PasswordRequestForm, donc attend 'username' et 'password'.
    """
    user = db.query(crud.models.User).filter(crud.models.User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    #access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}