from sqlalchemy import create_engine

DATABASE_URL = "postgresql://postgres:Motdepasse123@localhost:5433/motors"
engine = create_engine(DATABASE_URL)

try:
    connection = engine.connect()
    print("Connexion réussie ✅")
    connection.close()
except Exception as e:
    print("Erreur de connexion :", e)