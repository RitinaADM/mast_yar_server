from pydantic_settings import BaseSettings
from typing import Optional
from pydantic import ConfigDict

class Settings(BaseSettings):
    """
    Настройки приложения, загружаемые из переменных окружения.
    """
    # --- HTTP сервер ---
    host: str = "127.0.0.1"
    port: int = 8000

    # --- База данных ---
    db_url: str = "sqlite:///records.db"

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )

settings = Settings()