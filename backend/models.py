from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy import Enum
from backend.database import Base
import enum


# Utilisateurs

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=True)
    email = Column(String(150), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(20), default="client")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    dossiers = relationship("Dossier", back_populates="user", cascade="all, delete-orphan")
    rdv_essais = relationship("RdvEssai", back_populates="user", cascade="all, delete-orphan")



# Véhicules

class Vehicule(Base):
    __tablename__ = "vehicules"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String(50), nullable=False)
    model = Column(String(50), nullable=False)
    year = Column(Integer, nullable=True)
    price = Column(Float, nullable=False)
    kilometrage = Column(Integer, nullable=True)
    carburant = Column(String(20), nullable=True)
    transmission = Column(String(20), nullable=True)
    type = Column(String(20), nullable=True)  # exemple: "achat" / "location"
    description = Column(Text, nullable=True)
    image_url = Column(String, nullable=True)
    available = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    dossiers = relationship("Dossier", back_populates="vehicule", cascade="all, delete-orphan")
    rdv_essais = relationship("RdvEssai", back_populates="vehicule", cascade="all, delete-orphan")


# ------------------------
# Dossiers
# ------------------------
class DossierStatus(str, enum.Enum):
    EN_ATTENTE = "EN_ATTENTE"
    VALIDE = "VALIDE"
    REFUSE = "REFUSE"

class Dossier(Base):
    __tablename__ = "dossiers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    vehicule_id = Column(Integer, ForeignKey("vehicules.id"))
    type = Column(String(20), nullable=False)
    status = Column(Enum(DossierStatus), default=DossierStatus.EN_ATTENTE)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relations
    user = relationship("User", back_populates="dossiers")
    vehicule = relationship("Vehicule", back_populates="dossiers")
    documents = relationship("Document", back_populates="dossier", cascade="all, delete-orphan")


# ------------------------
# Documents uploadés
# ------------------------
class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    dossier_id = Column(Integer, ForeignKey("dossiers.id", ondelete="CASCADE"))
    document_type = Column(String(50), nullable=True)
    file_url = Column(String, nullable=False)
    uploaded_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    dossier = relationship("Dossier", back_populates="documents")


# ------------------------
# Rendez-vous essai
# ------------------------
class RdvStatus(str, enum.Enum):
    EN_ATTENTE = "EN_ATTENTE"
    CONFIRME = "CONFIRME"
    ANNULE = "ANNULE"

class RdvEssai(Base):
    __tablename__ = "rdv_essai"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    vehicule_id = Column(Integer, ForeignKey("vehicules.id"))
    date_rdv = Column(DateTime, nullable=False)
    status = Column(Enum(RdvStatus), default=RdvStatus.EN_ATTENTE)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="rdv_essais")
    vehicule = relationship("Vehicule", back_populates="rdv_essais")