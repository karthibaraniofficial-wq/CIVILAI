"""
CIVICFLOW AI — Application Configuration
"""
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    PROJECT_NAME: str = "CIVICFLOW AI"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # CORS Origins
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]
    
    # Database / Supabase
    DATABASE_URL: str = Field(default="", alias="DATABASE_URL")
    SUPABASE_URL: str = Field(default="", alias="SUPABASE_URL")
    SUPABASE_KEY: str = Field(default="", alias="SUPABASE_KEY")
    SUPABASE_SERVICE_ROLE_KEY: str = Field(default="", alias="SUPABASE_SERVICE_ROLE_KEY")
    # Auth & Security
    JWT_SECRET: str = Field(default="civicflow-super-secret-key-change-in-production-only", alias="JWT_SECRET")

    # AI / Gemini
    GEMINI_API_KEY: str = Field(default="", alias="GEMINI_API_KEY")
    GEMINI_MODEL: str = "gemini-3.8-flash"
    
    # Demo & Presentation Mode
    DEMO_MODE: bool = True
    SIMULATED_SLA_ACCELERATION: int = 60 # Factor to accelerate SLA for presentation
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()
