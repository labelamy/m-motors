from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class VehiculeBase(BaseModel):
    brand: str
    model: str
    price: float
    type: str  
    year: Optional[int] = None
    kilometrage: Optional[int] = None
    carburant: Optional[str] = None
    transmission: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    
class VehiculeCreate(VehiculeBase):
    pass

class VehiculeResponse(VehiculeBase):
    id: int
    available: bool
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: str
    name: Optional[str] = None
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str 

class DossierCreate(BaseModel):
    vehicule_id: int
    type: str

class DossierResponse(BaseModel):
    id: int
    user_id: int
    vehicule_id: int
    type: str
    status: str

    vehicule: VehiculeResponse

    class Config:
        from_attributes = True