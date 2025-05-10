from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    profile_picture: Optional[str] = "no_profile"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserProfile(BaseModel):
    id: UUID
    full_name: Optional[str] = None
    email: EmailStr
    created_at: Optional[datetime] = None
    images_uploaded_count: Optional[int] = 0
    has_entries: Optional[bool] = False
    profile_picture: Optional[str] = "no_profile"

class PasswordReset(BaseModel):
    email: EmailStr

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    profile_picture: Optional[str] = None 