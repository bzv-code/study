from __future__ import annotations

from datetime import datetime
from typing import Any

from models.stock_model import StockModel
from models.candle_model import CandleModel

from database.stock.stock_clickhouse import (
    StockClickHouse,
)

from database.duplicate_checker_clickhouse import (
    DuplicateCheckerClickHouse,
)

from utils.datetime_utils import (
    parse_moscow_datetime,
)

from utils.logger import get_logger


logger = get_logger(__name__)





class StockHWriterClickHouse:
    """
    Загрузчик недельных свечей акций MOEX
    в ClickHouse.


    Таблица:

        moex_api.moex_stock_h


    Источник:

        StockModel
        CandleModel


    Проверка дублей:

        secid + date

    """



    TABLE_NAME = "moex_api.moex_stock_h"



    BATCH_SIZE = 5000





    COLUMNS = [

        "secid",

        "isin",

        "shortname",

        "name",

        "sector",

        "engine",

        "market",

        "board",

        "date",

        "open",

        "high",

        "low",

        "close",

        "volume",

        "value",

    ]





    KEY_COLUMNS = [

        "secid",

        "date",

    ]







    def __init__(
        self,
        clickhouse: StockClickHouse,
    ) -> None:


        self.clickhouse = clickhouse



        self.duplicate_checker = DuplicateCheckerClickHouse(

            clickhouse.client

        )



        logger.debug(

            "StockHWriterClickHouse initialized TABLE=%s",

            self.TABLE_NAME,

        )







    @staticmethod
    def _parse_date(
        value: datetime,
    ) -> datetime:
        """
        Приведение даты MOEX
        к Europe/Moscow.
        """

        return parse_moscow_datetime(

            value

        )







    def _prepare_row(
        self,
        stock: StockModel,
        candle: CandleModel,
    ) -> list[Any]:
        """
        StockModel + CandleModel
        -> строка ClickHouse.
        """



        logger.debug(

            "PREPARE STOCK ROW SECID=%s DATE=%s",

            stock.secid,

            candle.begin,

        )



        return [


            stock.secid,


            stock.isin,


            stock.shortname,


            stock.name,


            stock.sector,



            stock.engine,


            stock.market,


            stock.board,



            self._parse_date(

                candle.begin

            ),



            candle.open,


            candle.high,


            candle.low,


            candle.close,



            candle.volume,


            candle.value,

        ]









    def write(
        self,
        stock: StockModel,
        candles: list[CandleModel],
    ) -> None:
        """
        Запись недельных свечей акций
        чанками в ClickHouse.
        """



        if not candles:


            logger.warning(

                "NO CANDLES FOR INSERT TABLE=%s",

                self.TABLE_NAME,

            )



            print(

                "NO DATA FOR INSERT"

            )



            return







        logger.info(

            "CLICKHOUSE STOCK INSERT START TABLE=%s INPUT=%s",

            self.TABLE_NAME,

            len(candles),

        )





        print("=" * 80)

        print(

            "CLICKHOUSE INSERT STOCK H"

        )

        print("=" * 80)







        rows = [


            self._prepare_row(

                stock,

                candle,

            )


            for candle in candles


        ]







        logger.debug(

            "ROWS PREPARED COUNT=%s",

            len(rows),

        )



        print(

            f"INPUT ROWS: {len(rows)}"

        )









        existing_keys = self.duplicate_checker.load_existing_keys(

            table=self.TABLE_NAME,

            key_columns=self.KEY_COLUMNS,

        )









        rows = self.duplicate_checker.filter_new_rows(

            rows=rows,

            columns=self.COLUMNS,

            existing_keys=existing_keys,

            key_columns=self.KEY_COLUMNS,

        )







        logger.info(

            "ROWS AFTER DUPLICATE CHECK COUNT=%s",

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

                "INSERT BATCH START=%s END=%s SIZE=%s",

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

                    "CLICKHOUSE STOCK INSERT ERROR TABLE=%s ERROR=%s",

                    self.TABLE_NAME,

                    error,

                )



                raise






            inserted += len(batch)









        logger.info(

            "CLICKHOUSE STOCK INSERT COMPLETE TABLE=%s INSERTED=%s",

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