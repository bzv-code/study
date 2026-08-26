from __future__ import annotations


from database.client_clickhouse import ClickHouseClient


from utils.logger import get_logger



logger = get_logger(__name__)





DATABASE_NAME = "moex_api"


TABLE_NAME = "moex_futures"



FULL_TABLE_NAME = (
    f"{DATABASE_NAME}.{TABLE_NAME}"
)







CREATE_DATABASE_SQL = f"""
CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}
"""







CREATE_TABLE_SQL = f"""
CREATE TABLE IF NOT EXISTS {FULL_TABLE_NAME}
(

    -- Идентификаторы

    secid String,

    board String,



    -- Названия

    shortname String,

    secname String,

    latname String,



    -- Базовый актив

    asset_code String,



    -- Тип инструмента

    sectype String,



    -- Цены

    prev_settle_price Float64,

    last_settle_price Float64,

    settle_price_clr Float64,

    prev_price Float64,



    -- Торговые параметры

    decimals Int32,

    min_step Float64,

    step_price Float64,

    lot_volume Int32,



    -- Маржинальные параметры

    initial_margin Float64,



    -- Лимиты

    high_limit Float64,

    low_limit Float64,



    -- Позиции

    prev_open_position Int64,



    -- Даты MOEX

    last_trade_date Date,

    last_delivery_date Date,



    -- Комиссии

    buy_sell_fee Float64,

    scalper_fee Float64,

    negotiated_fee Float64,

    exercise_fee Float64,



    -- Системное время загрузки

    load_datetime DateTime('Europe/Moscow')


)


ENGINE = MergeTree


ORDER BY
(
    asset_code,

    last_delivery_date,

    secid
)


SETTINGS
    index_granularity = 8192
"""









def main() -> None:
    """
    Создание ClickHouse таблицы:


        moex_api.moex_futures


    Назначение:


        Каталог фьючерсов MOEX FORTS


    Источник:


        FuturesCatalog


    Endpoint:


        /iss/engines/futures/markets/forts/securities.json


    Ключ:


        asset_code + last_delivery_date + secid

    """



    print("=" * 80)

    print(
        "CREATE CLICKHOUSE TABLE FUTURES"
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





if __name__ == "__main__":

    main()