from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float, Boolean
from database import Base
import enum
from sqlalchemy import Enum

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String, default="client")


class Vehicule(Base):
    __tablename__ = "vehicules"
    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String)
    model = Column(String)
    price = Column(Float)
    type = Column(String)
    available = Column(Boolean, default=True)

class DossierStatus(str, enum.Enum):
    EN_ATTENTE = "EN_ATTENTE"
    VALIDE = "VALIDE"
    REFUSE = "REFUSE"

class Dossier(Base):
    __tablename__ = "dossiers"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    vehicule_id = Column(Integer, ForeignKey("vehicules.id"))
    type = Column(String, nullable=False)
    status = Column(Enum(DossierStatus), default=DossierStatus.EN_ATTENTE)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
    document_path = Column(String, nullable=True)

