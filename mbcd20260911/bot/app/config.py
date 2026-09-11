"""Настройки бота MAX: токен, URL mini app, URL backend — из переменных окружения.

Bot() в maxapi 0.9.4 принимает токен позиционным аргументом (Bot(settings.bot_token)),
поэтому явно читаем его сами из MAX_BOT_TOKEN и передаём при создании бота в main.py.

Важно: os.getenv() сам по себе НЕ читает файл .env — переменную нужно либо
установить в системе, либо явно загрузить .env через python-dotenv (что мы
и делаем ниже). Без этого bot_token тут молча окажется пустой строкой.
"""
import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


def _load_env_file() -> None:
    """Ищет .env в нескольких вероятных местах: корень проекта, infra/, bot/."""
    bot_dir = Path(__file__).resolve().parents[1]  # app -> bot
    project_root = bot_dir.parent

    candidates = [
        project_root / ".env",
        project_root / "infra" / ".env",
        bot_dir / ".env",
    ]
    for path in candidates:
        if path.exists():
            load_dotenv(path)
            return


_load_env_file()


@dataclass
class Settings:
    bot_token: str = os.getenv("MAX_BOT_TOKEN", "")
    bot_username: str = os.getenv("MAX_BOT_USERNAME", "dom_cvetov_bot")
    backend_base_url: str = os.getenv("BACKEND_BASE_URL", "http://backend:8000")

    @property
    def miniapp_deeplink(self) -> str:
        # Формат диплинка мини-приложения в MAX: https://max.ru/<botName>?startapp
        # Подробнее: https://dev.max.ru/docs/webapps/introduction
        return f"https://max.ru/{self.bot_username}?startapp"


settings = Settings()
