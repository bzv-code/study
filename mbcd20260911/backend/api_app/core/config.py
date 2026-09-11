"""Настройки backend: строка подключения к БД, секретный ключ, токен бота MAX, параметры платежей."""
from pathlib import Path

from pydantic_settings import BaseSettings


def _find_env_file() -> str | None:
    """Ищет .env в нескольких вероятных местах: корень проекта, infra/, backend/."""
    backend_dir = Path(__file__).resolve().parents[2]  # app/core -> app -> backend
    project_root = backend_dir.parent

    candidates = [
        project_root / ".env",
        project_root / "infra" / ".env",
        backend_dir / ".env",
    ]
    for path in candidates:
        if path.exists():
            return str(path)
    return None


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:postgres@db:5432/flowers"
    secret_key: str = "change_me"
    payment_provider_token: str = ""
    max_bot_token: str = ""  # нужен для валидации WebAppData из mini app
    auth_dev_bypass: bool = False  # ТОЛЬКО для локальной разработки вне MAX, см. .env.example

    class Config:
        env_file = _find_env_file()
        extra = "ignore"


settings = Settings()
