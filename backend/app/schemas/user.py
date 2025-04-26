# backend/app/schemas/user.py

from pydantic import BaseModel, EmailStr
from typing import Optional

class UserProfileResponse(BaseModel):
    id: int
    email: EmailStr
    name: str
    company: Optional[str] = None
    position: Optional[str] = None
    profile_photo_url: Optional[str] = None

    class Config:
        orm_mode = True

