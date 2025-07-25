from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, validator
from typing import List, Optional
import os

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Database
    DATABASE_URL: str

    # Redis
    REDIS_URL: str

    # Security
    ALGORITHM: str = "HS256"
    CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",") if i.strip()]
        return v

    # Financial Settings
    LATE_FEE_PERCENTAGE: float = 0.05
    GRACE_PERIOD_DAYS: int = 7

    # Audit & Compliance
    AUDIT_LOG_RETENTION_DAYS: int = 2555  # 7 years
    BACKUP_SCHEDULE: str = "0 2 * * *"  # Daily at 2 AM

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
