import face_recognition
import numpy as np
from typing import List

def get_face_embedding(image_path: str) -> List[float]:
    """
    Carga la imagen, detecta el rostro y devuelve el embedding
    (128-dim vector).
    """
    image = face_recognition.load_image_file(image_path)
    encs = face_recognition.face_encodings(image)
    if not encs:
        raise ValueError("No se detectó ningún rostro")
    return encs[0].tolist()

def match_embeddings(
    target: List[float],
    candidates: List[dict],
    threshold: float = 0.6) -> List[int]:
    """
    candidates: lista de dict { usuario_id, vector }
    Retorna lista de usuario_ids cuya distancia euclídea < threshold.
    """
    t = np.array(target)
    matches = []
    for c in candidates:
        v = np.array(c["vector"])
        dist = np.linalg.norm(t - v)
        if dist < threshold:
            matches.append(c["usuario_id"])
    return matches

