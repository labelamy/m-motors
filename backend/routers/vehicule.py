from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
import crud
import schemas 
from auth import get_current_admin

router = APIRouter(prefix="/vehicules", tags=["Vehicules"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.VehiculeResponse)
def create(
    vehicule: schemas.VehiculeCreate,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin)
):
    return crud.create_vehicule(db, vehicule)

@router.get("/", response_model=list[schemas.VehiculeResponse])
def read_all(db: Session = Depends(get_db)):
    return crud.get_vehicules(db)