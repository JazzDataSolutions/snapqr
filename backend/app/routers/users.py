# backend/app/routers/users.py

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlmodel import Session
from typing import Optional
import os
import uuid

from app.db import get_session
from app.models import User
from app.schemas.user import UserProfileResponse
from app.core.storage import upload_to_s3, generate_presigned_url

router = APIRouter()


@router.post(
    "/profile",
    response_model=UserProfileResponse,
    summary="Create or update user profile"
)
async def create_or_update_profile(
    user_id: int = Form(..., description="User ID to update"),
    name: str = Form(..., description="Full name"),
    company: Optional[str] = Form(None, description="Company"),
    position: Optional[str] = Form(None, description="Position"),
    file: Optional[UploadFile] = File(None, description="Profile photo"),
    session: Session = Depends(get_session)
):
    # Get existing user
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update fields
    user.name = name
    user.company = company
    user.position = position

    # If a file was uploaded, upload to S3/MinIO and generate a presigned URL
    if file:
        ext = file.filename.split(".")[-1]
        key = f"profiles/{user_id}/{uuid.uuid4()}.{ext}"
        tmp_path = f"/tmp/{uuid.uuid4()}.{ext}"
        with open(tmp_path, "wb") as f:
            f.write(await file.read())
        upload_to_s3(tmp_path, key)
        os.remove(tmp_path)
        user.profile_photo_url = generate_presigned_url(key)

    session.add(user)
    session.commit()
    session.refresh(user)

    return UserProfileResponse.from_orm(user)


@router.get(
    "/{user_id}",
    response_model=UserProfileResponse,
    summary="Get user profile"
)
def get_profile(
    user_id: int,
    session: Session = Depends(get_session)
):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserProfileResponse.from_orm(user)

