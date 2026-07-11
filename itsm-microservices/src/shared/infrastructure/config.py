from pydantic_settings import BaseSettings
from typing import Optional, List


class Settings(BaseSettings):
  database_url: str = "postgresql+asyncpg://itsm_user:itsm_password@localhost:5432/itsm_db"
  environment: str = "development"
  debug: bool = True
  log_level: str = "INFO"
  api_version: str = "v1"
  api_title: str = "ITSM Microservices API"
  api_description: str = "Cloud-native ITSM replacement with DDD and microservices"
  
  # CORS Configuration
  cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173,http://127.0.0.1:5173,http://localhost,http://127.0.0.1"
  cors_allow_credentials: bool = True
  cors_allow_methods: List[str] = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
  cors_allow_headers: List[str] = ["*"]
  cors_max_age: int = 3600

  @property
  def allowed_origins(self) -> List[str]:
    """Parse CORS origins from environment variable"""
    return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

  class Config:
    env_file = ".env"
    case_sensitive = False


settings = Settings()
