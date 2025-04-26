from pydantic import BaseSettings

class Settings(BaseSettings):
    POSTGRES_URL: str
    API_V1_STR: str = "/v1"
    PROJECT_NAME: str = "SnapQR MVP"
    JWT_SECRET_KEY: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str = "us-east-1"
    S3_BUCKET: str
    MINIO_USE: bool = False

    class Config:
        env_file = ".env"

settings = Settings()

