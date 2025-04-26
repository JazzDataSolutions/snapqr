# backend/app/schemas/user.py

from pydantic import BaseModel, EmailStr
from typing import Optional

class UserProfileResponse(BaseModel):
    id: int
    email: EmailStr
    nombre: str
    empresa: Optional[str] = None
    posicion: Optional[str] = None
    foto_perfil_url: Optional[str] = None

    class Config:
        orm_mode = True

