from fastapi import FastAPI
from database import engine, Base
import models
from routers import vehicule
from routers import user

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(vehicule.router, prefix="/vehicules", tags=["Vehicules"])

app.include_router(user.router, prefix="/auth", tags=["Auth"])

@app.get("/")
def root():
    return {"message": "API M-Motors opérationnelle 🚗"}