from __future__ import annotations


from database.client_clickhouse import ClickHouseClient

from utils.logger import get_logger



logger = get_logger(__name__)





TABLE_NAME = "moex_api.moex_currency_m10"





def main() -> None:
    """
    Создание таблицы свечей валют MOEX.


    Таблица:

        moex_api.moex_currency_m10


    Таймфрейм:

        interval=10


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
            f"TABLE: {TABLE_NAME}"
        )


        print()



        # --------------------------------------------------
        # Создание таблицы
        # --------------------------------------------------

        print(
            "CREATE TABLE..."
        )



        sql = f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME}
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



        client.execute(
            sql
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