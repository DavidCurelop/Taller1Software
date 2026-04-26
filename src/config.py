"""Configuracion global de la aplicacion."""

from dataclasses import dataclass
import os

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    """Configuraciones de entorno para la aplicacion."""

    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./data/ecommerce_chat.db")
    environment: str = os.getenv("ENVIRONMENT", "development")


settings = Settings()
