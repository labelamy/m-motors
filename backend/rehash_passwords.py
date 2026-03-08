from backend.database import SessionLocal
from backend import crud

db = SessionLocal()
crud.rehash_existing_users(db)
db.close()

print("Tous les mots de passe ont été rehashés !")