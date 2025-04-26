# backend/app/routers/users.py

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlmodel import Session
from typing import Optional
import os
import uuid

from app.db import get_session
from app.models import Usuario
from app.schemas.user import UserProfileResponse
from app.core.storage import upload_to_s3, generate_presigned_url

router = APIRouter()


@router.post(
    "/profile",
    response_model=UserProfileResponse,
    summary="Crear o actualizar perfil de usuario"
)
async def create_or_update_profile(
    user_id: int = Form(..., description="ID del usuario a actualizar"),
    nombre: str = Form(..., description="Nombre completo"),
    empresa: Optional[str] = Form(None, description="Empresa"),
    posicion: Optional[str] = Form(None, description="Posición"),
    file: Optional[UploadFile] = File(None, description="Foto de perfil"),
    session: Session = Depends(get_session)
):
    # Buscar usuario existente
    user = session.get(Usuario, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Actualizar campos
    user.nombre = nombre
    user.empresa = empresa
    user.posicion = posicion

    # Si se envió una foto, subir a S3/MinIO y generar URL presignada
    if file:
        ext = file.filename.split(".")[-1]
        key = f"profiles/{user_id}/{uuid.uuid4()}.{ext}"
        tmp_path = f"/tmp/{uuid.uuid4()}.{ext}"
        with open(tmp_path, "wb") as f:
            f.write(await file.read())
        upload_to_s3(tmp_path, key)
        os.remove(tmp_path)
        user.foto_perfil_url = generate_presigned_url(key)

    session.add(user)
    session.commit()
    session.refresh(user)

    return UserProfileResponse.from_orm(user)


@router.get(
    "/{user_id}",
    response_model=UserProfileResponse,
    summary="Obtener perfil de usuario"
)
def get_profile(
    user_id: int,
    session: Session = Depends(get_session)
):
    user = session.get(Usuario, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return UserProfileResponse.from_orm(user)

