from fastapi import FastAPI
from database import engine
import models
from routers import vehicule, user, dossiers

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(vehicule.router, prefix="/vehicules", tags=["Vehicules"])

app.include_router(user.router, prefix="/auth", tags=["Auth"])
app.include_router(dossiers.router)

@app.get("/")
def root():
    return {"message": "API M-Motors opérationnelle 🚗"}