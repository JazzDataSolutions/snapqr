# backend/app/schemas/qr.py

from pydantic import BaseModel
from typing import Dict

class QRGenerateResponse(BaseModel):
    qr_url: str
    qr_data: Dict[str, str]

    class Config:
        schema_extra = {
            "example": {
                "qr_url": "https://example-bucket.s3.amazonaws.com/qr/1/abcd-1234.png",
                "qr_data": {
                    "id": "1",
                    "nombre": "Juan Pérez",
                    "email": "juan.perez@example.com"
                }
            }
        }

