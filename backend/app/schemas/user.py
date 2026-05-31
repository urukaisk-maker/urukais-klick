"""
Esquemas de usuario para validación y serialización
"""

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    alias: str
    email: EmailStr

class UserCreate(UserBase):
    password: Optional[str] = None

class UserUpdate(BaseModel):
    alias: Optional[str] = None
    email: Optional[EmailStr] = None
    is_artist: Optional[bool] = None
    artist_bio: Optional[str] = None
    artist_links: Optional[str] = None

class UserInDB(UserBase):
    id: int
    is_artist: bool
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class User(UserInDB):
    pass
