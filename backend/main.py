from fastapi import FastAPI, Request
from database import engine
import models
from routers import vehicule, user, dossiers
from fastapi.responses import JSONResponse
from logging_config import logger

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(vehicule.router, prefix="/vehicules", tags=["Vehicules"])

app.include_router(user.router, prefix="/auth", tags=["Auth"])
app.include_router(dossiers.router)

@app.get("/")
def root():
    return {"message": "API M-Motors opérationnelle 🚗"}

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Erreur serveur: {str(exc)}")

    return JSONResponse(
        status_code=500,
        content={"detail": "Erreur interne du serveur"}
    )