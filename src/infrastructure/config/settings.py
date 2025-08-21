from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # --- HTTP server ---
    host: str = "127.0.0.1"
    port: int = 8000

    # --- Database ---
    db_url: str = "sqlite:///records.db"

    class Config:
        env_file = ".env"   # будем брать переменные из файла
        env_file_encoding = "utf-8"


settings = Settings()
