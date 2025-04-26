import face_recognition
import numpy as np
from typing import List

def get_face_embedding(image_path: str) -> List[float]:
    """
    Load the image, detect the face, and return the embedding
    (128-dimensional vector).
    """
    image = face_recognition.load_image_file(image_path)
    encs = face_recognition.face_encodings(image)
    if not encs:
        raise ValueError("No face detected")
    return encs[0].tolist()

def match_embeddings(
    target: List[float],
    candidates: List[dict],
    threshold: float = 0.6) -> List[int]:
    """
    candidates: list of dicts { user_id, vector }
    Returns a list of user_ids whose Euclidean distance < threshold.
    """
    t = np.array(target)
    matches = []
    for c in candidates:
        v = np.array(c["vector"])
        dist = np.linalg.norm(t - v)
        if dist < threshold:
            matches.append(c["user_id"])
    return matches

