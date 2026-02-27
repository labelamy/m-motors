from sqlalchemy.orm import Session
import models
import schemas
from auth import hash_password, verify_password

def create_vehicule(db: Session, vehicule: schemas.VehiculeCreate):
    db_vehicule = models.Vehicule(**vehicule.dict())
    db.add(db_vehicule)
    db.commit()
    db.refresh(db_vehicule)
    return db_vehicule

def get_vehicules(db: Session):
    return db.query(models.Vehicule).all()

def create_user(db, user):
    hashed_pwd = hash_password(user.password)
    db_user = models.User(email=user.email, password=hashed_pwd)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db, email, password):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user