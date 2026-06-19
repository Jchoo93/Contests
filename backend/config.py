from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    eia_api_key: str
    database_url: str = "sqlite:///./power_grid.db"
    environment: str = "development"
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True
    cors_origins: list = ["http://localhost:3000", "http://localhost:5173"]
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
