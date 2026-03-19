# routers/seed_images.py
from fastapi import APIRouter
import subprocess
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/seed-images")
def seed_images():
    try:
        # Appelle le script update_images.py
        subprocess.run(["python", "update_images.py"], check=True)
        return JSONResponse({"status": "Migration images terminée ✅"})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)