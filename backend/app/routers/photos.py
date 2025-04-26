from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlmodel import Session, select
import uuid, os

from app.db import get_session
from app.models import FotoEvento, Embedding, FotoUsuarioLink
from app.core.face import get_face_embedding, match_embeddings
from app.core.storage import upload_to_s3

router = APIRouter()

@router.post("/upload")
async def upload_photo(
    file: UploadFile = File(...),
    session: Session = Depends(get_session)
):
    # 1) Guardar raw en /tmp
    tmp_path = f"/tmp/{uuid.uuid4()}.jpg"
    with open(tmp_path, "wb") as f:
        f.write(await file.read())

    # 2) Subir a S3
    s3_key = f"raw/{os.path.basename(tmp_path)}"
    await upload_to_s3(tmp_path, s3_key)
    os.remove(tmp_path)

    # 3) Registrar foto_evento
    foto = FotoEvento(s3_key=s3_key)
    session.add(foto)
    session.commit()
    session.refresh(foto)

    # 4) Generar embeddings del raw local
    local_raw = f"/tmp/{foto.id}.jpg"
    
    # Descarga temporal para procesar
    await download_from_s3(s3_key, local_raw)
    emb = get_face_embedding(local_raw)
    os.remove(local_raw)

    # 5) Cargar todos los embeddings registrados
    candidates = session.exec(select(Embedding)).all()
    cands = [ {"usuario_id": e.usuario_id, "vector": e.vector} for e in candidates ]

    # 6) Emparejar
    matched_ids = match_embeddings(emb, cands)

    # 7) Insertar links
    for uid in set(matched_ids):
        link = FotoUsuarioLink(foto_id=foto.id, usuario_id=uid)
        session.add(link)
    session.commit()

    return {"fotoId": foto.id, "usuarios_detectados": matched_ids}

