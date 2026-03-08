from backend.database import SessionLocal
from backend.models import Vehicule

db = SessionLocal()
vehicules = db.query(Vehicule).all()
for v in vehicules:
    print({column.name: getattr(v, column.name) for column in v.__table__.columns})

db.close()