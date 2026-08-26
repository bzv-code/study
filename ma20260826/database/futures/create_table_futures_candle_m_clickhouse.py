
from __future__ import annotations

from database.client_clickhouse import ClickHouseClient

from utils.logger import get_logger


logger = get_logger(__name__)


# ======================================================
# DATABASE
# ======================================================

DATABASE_NAME = "moex_api"

TABLE_NAME = "moex_futures_candle_m"

FULL_TABLE_NAME = (
    f"{DATABASE_NAME}.{TABLE_NAME}"
)


# ======================================================
# CREATE DATABASE
# ======================================================

CREATE_DATABASE_SQL = f"""
CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}
"""


# ======================================================
# CREATE TABLE
# ======================================================

CREATE_TABLE_SQL = f"""
CREATE TABLE IF NOT EXISTS {FULL_TABLE_NAME}
(

    -- ==================================================
    -- Идентификатор фьючерса
    -- ==================================================

    secid String,

    board String,


    -- ==================================================
    -- Базовый актив
    -- ==================================================

    asset_code String,


    -- ==================================================
    -- Сектор
    -- ==================================================

    sector String,


    -- ==================================================
    -- Время начала месячной свечи MOEX
    -- ==================================================

    date DateTime('Europe/Moscow'),


    -- ==================================================
    -- OHLC
    -- ==================================================

    open Float64,

    high Float64,

    low Float64,

    close Float64,


    -- ==================================================
    -- Объемы торгов
    -- ==================================================

    volume UInt64,

    value Float64

)

ENGINE = MergeTree

ORDER BY
(
    secid,
    date
)

SETTINGS
    index_granularity = 8192
"""


# ======================================================
# MAIN
# ======================================================

def main() -> None:
    """
    Создание ClickHouse таблицы:

        moex_api.moex_futures_candle_m


    Назначение:

        Месячные свечи (M)
        бессрочных фьючерсов MOEX.


    Источник:

        FuturesCandleService


    Таймфрейм:

        interval=31


    Время:

        Europe/Moscow


    Ключ:

        secid + date


    Поля:

        secid
        board
        asset_code
        sector
        date
        open
        high
        low
        close
        volume
        value


    Примечание:

        Поле date содержит дату и время
        начала месячной свечи.
    """

    print("=" * 80)

    print(
        "CREATE CLICKHOUSE TABLE FUTURES MONTHLY"
    )

    print("=" * 80)


    client = ClickHouseClient()


    try:

        # --------------------------------------------------
        # Information
        # --------------------------------------------------

        print(
            f"DATABASE: {DATABASE_NAME}"
        )

        print(
            f"TABLE   : {FULL_TABLE_NAME}"
        )

        print(
            "INTERVAL: 31"
        )

        print()


        # --------------------------------------------------
        # Database
        # --------------------------------------------------

        print(
            "CREATE DATABASE..."
        )


        client.execute(
            CREATE_DATABASE_SQL
        )


        print(
            "DATABASE STATUS: OK"
        )

        print()


        # --------------------------------------------------
        # Table
        # --------------------------------------------------

        print(
            "CREATE TABLE..."
        )


        client.execute(
            CREATE_TABLE_SQL
        )


        print(
            "TABLE STATUS: OK"
        )


    finally:

        client.close()


    print()

    print("=" * 80)

    print(
        "COMPLETE"
    )

    print("=" * 80)


# ======================================================
# ENTRY POINT
# ======================================================

if __name__ == "__main__":
    main()

