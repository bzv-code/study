from pathlib import Path

from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):

    # MAX BOT

    MAX_TOKEN: str
    BOT_NAME: str = "Биржевой помощник FINAM"

    # CLICKHOUSE

    CLICKHOUSE_HOST: str
    CLICKHOUSE_PORT: int = 8123
    CLICKHOUSE_USER: str = "default"
    CLICKHOUSE_PASSWORD: str = ""
    CLICKHOUSE_DATABASE: str

    # POSTGRESQL

    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DATABASE: str

    # =====================================
    # ALERTS
    # =====================================

    # период проверки уведомлений

    price_alert_check_interval: int = 3600

    class Config:

        env_file = BASE_DIR / ".env"
        env_file_encoding = "utf-8"


settings = Settings()