# app/schemas.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr  # <-- 1. Import EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr  # <-- 2. Apply EmailStr here
    date: datetime
    password: str
    domain: str

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None  # <-- 3. Apply EmailStr here as well
    date: Optional[datetime] = None
    password: Optional[str] = None
    domain: Optional[str] = None

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: int
    name: str
    date: Optional[datetime] = None
    email: EmailStr  # <-- 4. Optional: Use EmailStr for responses too
    domain: str

    class Config:
        from_attributes = True