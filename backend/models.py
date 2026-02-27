from sqlalchemy import Column, Integer, String, Float, Boolean
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String, default="client")  # client ou admin

class Vehicule(Base):
    __tablename__ = "vehicules"
    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String)
    model = Column(String)
    price = Column(Float)
    type = Column(String)  # achat ou location
    available = Column(Boolean, default=True)

class Dossier(Base):
    __tablename__ = "dossiers"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    vehicle_id = Column(Integer)
    status = Column(String, default="en_cours")  # en_cours, accepte, refuse