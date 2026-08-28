from __future__ import annotations


from datetime import datetime

from typing import Any


from models.futures_model import FuturesModel


from database.futures.futures_clickhouse import (
    FuturesClickHouse,
)


from database.duplicate_checker_clickhouse import (
    DuplicateCheckerClickHouse,
)


from utils.logger import get_logger



logger = get_logger(__name__)







class FuturesWriterClickHouse:
    """
    Загрузчик каталога фьючерсов MOEX
    в ClickHouse.


    Таблица:

        moex_api.moex_futures


    Источник:

        FuturesModel


    Проверка дублей:

        secid + board

    """



    TABLE_NAME = "moex_api.moex_futures"


    BATCH_SIZE = 5000







    COLUMNS = [

        "secid",

        "board",

        "shortname",

        "secname",

        "latname",

        "asset_code",

        "sectype",


        "prev_settle_price",

        "last_settle_price",

        "settle_price_clr",

        "prev_price",


        "decimals",

        "min_step",

        "step_price",

        "lot_volume",


        "initial_margin",


        "high_limit",

        "low_limit",


        "prev_open_position",


        "last_trade_date",

        "last_delivery_date",


        "buy_sell_fee",

        "scalper_fee",

        "negotiated_fee",

        "exercise_fee",


        "load_datetime",

    ]






    KEY_COLUMNS = [

        "secid",

        "board",

    ]









    def __init__(
        self,
        clickhouse: FuturesClickHouse,
    ) -> None:


        self.clickhouse = clickhouse



        self.duplicate_checker = (
            DuplicateCheckerClickHouse(
                clickhouse.client
            )
        )



        logger.debug(

            "FuturesWriterClickHouse initialized TABLE=%s",

            self.TABLE_NAME,

        )









    def _prepare_row(
        self,
        future: FuturesModel,
        load_datetime: datetime,
    ) -> list[Any]:
        """
        FuturesModel -> ClickHouse row.
        """



        logger.debug(

            "PREPARE FUTURES ROW SECID=%s",

            future.secid,

        )



        return [


            future.secid,


            future.board,


            future.shortname,


            future.secname,


            future.latname,


            future.asset_code,


            future.sectype,



            future.prev_settle_price,


            future.last_settle_price,


            future.settle_price_clr,


            future.prev_price,



            future.decimals,


            future.min_step,


            future.step_price,


            future.lot_volume,



            future.initial_margin,



            future.high_limit,


            future.low_limit,



            future.prev_open_position,



            future.last_trade_date,


            future.last_delivery_date,



            future.buy_sell_fee,


            future.scalper_fee,


            future.negotiated_fee,


            future.exercise_fee,



            load_datetime,

        ]









    def write(
        self,
        futures: list[FuturesModel],
    ) -> None:
        """
        Запись фьючерсов чанками
        в ClickHouse.
        """



        if not futures:


            logger.warning(

                "NO FUTURES FOR INSERT TABLE=%s",

                self.TABLE_NAME,

            )


            print(
                "NO DATA FOR INSERT"
            )


            return








        logger.info(

            "CLICKHOUSE FUTURES INSERT START TABLE=%s INPUT=%s",

            self.TABLE_NAME,

            len(futures),

        )





        print("=" * 80)

        print(
            "CLICKHOUSE INSERT FUTURES"
        )

        print("=" * 80)







        load_datetime = datetime.now()






        rows = [


            self._prepare_row(

                future,

                load_datetime,

            )


            for future in futures

        ]







        logger.debug(

            "FUTURES ROWS PREPARED COUNT=%s",

            len(rows),

        )





        print(

            f"INPUT ROWS: {len(rows)}"

        )









        existing_keys = (
            self.duplicate_checker.load_existing_keys(

                table=self.TABLE_NAME,

                key_columns=self.KEY_COLUMNS,

            )
        )








        rows = (
            self.duplicate_checker.filter_new_rows(

                rows=rows,

                columns=self.COLUMNS,

                existing_keys=existing_keys,

                key_columns=self.KEY_COLUMNS,

            )
        )








        logger.info(

            "FUTURES ROWS AFTER DUPLICATE CHECK COUNT=%s",

            len(rows),

        )








        if not rows:


            print(
                "NOTHING TO INSERT"
            )


            return









        inserted = 0








        for start in range(

            0,

            len(rows),

            self.BATCH_SIZE,

        ):



            end = min(

                start + self.BATCH_SIZE,

                len(rows),

            )



            batch = rows[start:end]








            logger.debug(

                "INSERT FUTURES BATCH START=%s END=%s SIZE=%s",

                start,

                end,

                len(batch),

            )




            print(

                f"INSERT BATCH: {start} - {end}"

            )








            try:



                self.clickhouse.insert(

                    data=batch,

                    columns=self.COLUMNS,

                )





            except Exception as error:



                logger.exception(

                    "CLICKHOUSE FUTURES INSERT ERROR TABLE=%s ERROR=%s",

                    self.TABLE_NAME,

                    error,

                )



                raise








            inserted += len(batch)









        logger.info(

            "CLICKHOUSE FUTURES INSERT COMPLETE TABLE=%s INSERTED=%s",

            self.TABLE_NAME,

            inserted,

        )








        print()

        print(
            f"INSERTED: {inserted}"
        )

        print(
            "STATUS: OK"
        )

        print("=" * 80)