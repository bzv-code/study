# moex_api/database/stock_foreign/create_table_stock_foreign_m1_clickhouse.py
from __future__ import annotations

from database.client_clickhouse import ClickHouseClient
from utils.logger import get_logger

logger = get_logger(__name__)

DATABASE_NAME = "moex_api"
TABLE_NAME = "moex_stock_foreign_m1"

FULL_TABLE_NAME = f"{DATABASE_NAME}.{TABLE_NAME}"

CREATE_DATABASE_SQL = f"""
CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}
"""

CREATE_TABLE_SQL = f"""
CREATE TABLE IF NOT EXISTS {FULL_TABLE_NAME}
(
    -- Идентификаторы акции
    secid String,
    isin String,

    -- Название
    shortname String,

    -- Классификация
    sector String,
    country String,

    -- Торговая инфраструктура
    engine String,
    market String,
    board String,

    -- Время MOEX
    date DateTime('Europe/Moscow'),

    -- OHLC
    open Float64,
    high Float64,
    low Float64,
    close Float64,

    -- Объемы
    volume UInt64,
    value Float64
)
ENGINE = MergeTree
ORDER BY (secid, date)
SETTINGS index_granularity = 8192
"""


def main() -> None:
    """
    Создание ClickHouse таблицы:
        moex_api.moex_stock_foreign_m1

    Назначение:
        Минутные свечи зарубежных акций MOEX

    Таймфрейм:
        interval=1

    Время:
        Europe/Moscow

    Ключ:
        secid + date
    """
    print("=" * 80)
    print("CREATE CLICKHOUSE TABLE STOCK FOREIGN M1")
    print("=" * 80)

    client = ClickHouseClient()

    try:
        print(f"DATABASE: {DATABASE_NAME}")
        print(f"TABLE   : {FULL_TABLE_NAME}")
        print()

        print("CREATE DATABASE...")
        client.execute(CREATE_DATABASE_SQL)
        print("DATABASE STATUS: OK\n")

        print("CREATE TABLE...")
        client.execute(CREATE_TABLE_SQL)
        print("TABLE STATUS: OK\n")

    finally:
        client.close()

    print("=" * 80)
    print("COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()