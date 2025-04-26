# backend/app/routers/qr.py

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import Dict
import qrcode
import io
import uuid
import os

from app.db import get_session
from app.models import User, QRContact
from app.schemas.qr import QRGenerateResponse
from app.core.storage import upload_to_s3, generate_presigned_url

router = APIRouter()


@router.post(
    "/{user_id}",
    response_model=QRGenerateResponse,
    summary="Generate QR code for a user"
)
async def generate_qr(
    user_id: int,
    session: Session = Depends(get_session)
):
    # Verify user exists
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Prepare JSON payload for QR
    data: Dict[str, str] = {
        "id": str(user.id),
        "name": user.name,
        "email": user.email
    }

    # 3) Generar imagen QR en memoria
    qr_img = qrcode.make(data)
    buf = io.BytesIO()
    qr_img.save(buf, format="PNG")
    buf.seek(0)

    # 4) Subir la imagen a S3/MinIO
    key = f"qr/{user_id}/{uuid.uuid4()}.png"
    tmp_path = f"/tmp/{uuid.uuid4()}.png"
    with open(tmp_path, "wb") as f:
        f.write(buf.getvalue())
    upload_to_s3(tmp_path, key)
    os.remove(tmp_path)

    # 5) Generar URL presignada
    url = generate_presigned_url(key)

    # Save record in qr_contact table
    qr_record = QRContact(
        user_id=user_id,
        qr_data=data,
        qr_url=url
    )
    session.add(qr_record)
    session.commit()
    session.refresh(qr_record)

    # 7) Devolver respuesta con URL y datos
    return QRGenerateResponse(
        qr_url=url,
        qr_data=data
    )

