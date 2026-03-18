from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from typing import Optional

import schemas 
import crud 
from database import get_db
from auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, verify_password

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
def login(data: dict = Body(...), db: Session = Depends(get_db)):
    email = data.get("email")
    password = data.get("password")
    user = crud.authenticate_user(db, email, password)
    
    if not user :
        raise HTTPException(
            status_code=401,
            detail="Email ou mot de passe incorrect",
            
        )
    
    #access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role},
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


# LOGIN Swagger (OAuth2PasswordRequestForm)
# --------------------------------------------
@router.post("/login-swagger", response_model=schemas.Token)
def login_swagger(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Login compatible Swagger avec form-data
    """
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")

    access_token = create_access_token(
        data={"sub": user.email, "role": user.role}
    )

    return {"access_token": access_token, "token_type": "bearer"}