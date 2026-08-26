from __future__ import annotations

from database.client_clickhouse import ClickHouseClient



DATABASE_NAME = "moex_api"

TABLE_NAME = "moex_metal_h1"



FULL_TABLE_NAME = (

    f"{DATABASE_NAME}.{TABLE_NAME}"

)



CREATE_DATABASE_SQL = f"""
CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}
"""



CREATE_TABLE_SQL = f"""
CREATE TABLE IF NOT EXISTS {FULL_TABLE_NAME}
(

    ticker String,

    name String,

    engine String,

    market String,

    board String,


    -- Московское время MOEX
    date DateTime('Europe/Moscow'),


    open Float64,

    high Float64,

    low Float64,

    close Float64,


    volume UInt64,

    value Float64

)

ENGINE = MergeTree

ORDER BY
(
    ticker,

    date
)

SETTINGS
    index_granularity = 8192
"""



def main() -> None:
    """
    Создание таблицы:

        moex_api.moex_metal_h1


    Таймфрейм:

        1 час


    Время:

        Europe/Moscow


    Ключ:

        ticker + date

    """


    print("=" * 80)

    print(
        "CREATE CLICKHOUSE TABLE"
    )

    print("=" * 80)



    client = ClickHouseClient()



    try:


        print(
            f"DATABASE: {DATABASE_NAME}"
        )


        print(
            f"TABLE   : {FULL_TABLE_NAME}"
        )


        print()



        # --------------------------------------------------
        # Создание базы
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
        # Создание таблицы
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



if __name__ == "__main__":

    main()