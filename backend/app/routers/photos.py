from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlmodel import Session, select
import uuid, os

from app.db import get_session
from app.models import EventPhoto, Embedding, PhotoUserLink
from app.core.face import get_face_embedding, match_embeddings
from app.core.storage import upload_to_s3, download_from_s3

router = APIRouter()

@router.post(
    "/upload",
    summary="Upload event photo, extract face embeddings, and match to users"
)
async def upload_photo(
    file: UploadFile = File(...),
    session: Session = Depends(get_session)
):
    # 1) Save uploaded file to a temporary path
    tmp_path = f"/tmp/{uuid.uuid4()}.jpg"
    with open(tmp_path, "wb") as f:
        f.write(await file.read())

    # 2) Upload raw file to S3/MinIO
    s3_key = f"raw/{os.path.basename(tmp_path)}"
    # Raw file uploaded to S3/MinIO
    upload_to_s3(tmp_path, s3_key)
    os.remove(tmp_path)

    # 3) Create event photo record
    photo = EventPhoto(s3_key=s3_key)
    session.add(photo)
    session.commit()
    session.refresh(photo)

    # 4) Download file for processing and generate face embedding
    local_raw = f"/tmp/{photo.id}.jpg"
    
    # Temporary download for embedding extraction
    download_from_s3(s3_key, local_raw)
    emb = get_face_embedding(local_raw)
    os.remove(local_raw)

    # 5) Load all registered embeddings
    candidates = session.exec(select(Embedding)).all()
    cands = [{"user_id": e.user_id, "vector": e.vector} for e in candidates]

    # 6) Match embeddings against candidates
    matched_ids = match_embeddings(emb, cands)

    # 7) Insert links between photo and matched users
    for uid in set(matched_ids):
        link = PhotoUserLink(photo_id=photo.id, user_id=uid)
        session.add(link)
    session.commit()

    return {"photo_id": photo.id, "detected_user_ids": matched_ids}

