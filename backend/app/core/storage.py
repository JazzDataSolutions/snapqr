# backend/app/core/storage.py

import os
import boto3
from botocore.client import Config
from app.config import settings

def get_s3_client():
    """
    Crea y retorna un cliente S3 o MinIO basado en la configuración.
    """
    if settings.MINIO_USE:
        endpoint = os.getenv("MINIO_ENDPOINT", "http://minio:9000")
        return boto3.client(
            "s3",
            endpoint_url=endpoint,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            config=Config(signature_version="s3v4"),
            region_name=settings.AWS_REGION,
        )
    # AWS S3
    return boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION,
    )

def upload_to_s3(file_path: str, key: str) -> str:
    """
    Sube un archivo local a S3/MinIO y retorna la clave del objeto.
    """
    client = get_s3_client()
    bucket = settings.S3_BUCKET
    client.upload_file(file_path, bucket, key)
    return key

def download_from_s3(key: str, download_path: str) -> None:
    """
    Descarga un objeto de S3/MinIO a una ruta local.
    """
    client = get_s3_client()
    bucket = settings.S3_BUCKET
    client.download_file(bucket, key, download_path)

def generate_presigned_url(key: str, expires_in: int = 3600) -> str:
    """
    Genera una URL presignada para descarga de un objeto.
    """
    client = get_s3_client()
    return client.generate_presigned_url(
        "get_object",
        Params={"Bucket": settings.S3_BUCKET, "Key": key},
        ExpiresIn=expires_in
    )

