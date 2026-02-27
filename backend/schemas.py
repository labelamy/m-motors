from pydantic import BaseModel, EmailStr
from typing import Optional

class VehiculeBase(BaseModel):
    brand: str
    model: str
    price: float
    type: str  # achat ou location

class VehiculeCreate(VehiculeBase):
    pass

class VehiculeResponse(VehiculeBase):
    id: int
    available: bool

    class Config:
        orm_mode = True
        

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

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str