from __future__ import annotations

import os

from dotenv import load_dotenv


load_dotenv()


class ClickHouseConfig:
    """
    Конфигурация ClickHouse.
    """

    HOST = os.getenv("CLICKHOUSE_HOST", "localhost")

    PORT = int(
        os.getenv(
            "CLICKHOUSE_PORT",
            "8123",
        )
    )

    USER = os.getenv(
        "CLICKHOUSE_USER",
        "default",
    )

    PASSWORD = os.getenv(
        "CLICKHOUSE_PASSWORD",
        "",
    )

    DATABASE = os.getenv(
        "CLICKHOUSE_DATABASE",
        "moex",
    )