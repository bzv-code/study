from __future__ import annotations

from datetime import datetime
from typing import Any


from models.metal_model import MetalModel

from database.metal.metal_clickhouse import MetalClickHouse
from database.duplicate_checker_clickhouse import DuplicateCheckerClickHouse

from utils.datetime_utils import parse_moscow_datetime
from utils.logger import get_logger



logger = get_logger(__name__)





class MetalMWriterClickHouse:
    """
    Загрузчик месячных свечей металлов MOEX
    в ClickHouse.


    Таблица:

        moex_api.moex_metal_m


    Таймфрейм:

        1 месяц


    MOEX ISS interval:

        31


    Проверка дублей:

        ticker + date

    """



    TABLE_NAME = "moex_api.moex_metal_m"



    BATCH_SIZE = 5000



    COLUMNS = [

        "ticker",

        "name",

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

        "ticker",

        "date",

    ]



    def __init__(
        self,
        clickhouse: MetalClickHouse,
    ) -> None:

        self.clickhouse = clickhouse


        self.duplicate_checker = DuplicateCheckerClickHouse(

            clickhouse.client

        )


        logger.debug(
            "MetalMWriterClickHouse initialized TABLE=%s",
            self.TABLE_NAME,
        )



    @staticmethod
    def _parse_date(
        value: str | datetime,
    ) -> datetime:
        """
        Приведение даты MOEX
        к московскому времени.
        """

        return parse_moscow_datetime(

            value

        )



    def _prepare_row(
        self,
        item: MetalModel,
    ) -> list[Any]:
        """
        MetalModel -> строка ClickHouse.
        """

        return [

            item.ticker,

            item.name,

            item.engine,

            item.market,

            item.board,


            self._parse_date(

                item.date

            ),


            item.open,

            item.high,

            item.low,

            item.close,

            item.volume,

            item.value,

        ]



    def write(
        self,
        metals: list[MetalModel],
    ) -> None:
        """
        Запись месячных свечей чанками.


        Перед вставкой:

        - подготовка даты MOEX;
        - проверка существующих записей;
        - удаление дублей внутри пакета;
        - пакетная вставка.

        """


        logger.info(

            "START INSERT METAL M TABLE=%s INPUT=%s",

            self.TABLE_NAME,

            len(metals),

        )



        if not metals:


            logger.warning(

                "NO DATA FOR INSERT TABLE=%s",

                self.TABLE_NAME,

            )

            return



        rows = [

            self._prepare_row(

                item

            )

            for item in metals

        ]



        logger.debug(

            "PREPARED ROWS COUNT=%s",

            len(rows),

        )



        existing_keys = self.duplicate_checker.load_existing_keys(

            table=self.TABLE_NAME,

            key_columns=self.KEY_COLUMNS,

        )



        logger.debug(

            "EXISTING KEYS COUNT=%s",

            len(existing_keys),

        )



        rows = self.duplicate_checker.filter_new_rows(

            rows=rows,

            columns=self.COLUMNS,

            existing_keys=existing_keys,

            key_columns=self.KEY_COLUMNS,

        )



        if not rows:


            logger.info(

                "NOTHING TO INSERT TABLE=%s",

                self.TABLE_NAME,

            )

            return



        logger.info(

            "READY INSERT ROWS=%s TABLE=%s",

            len(rows),

            self.TABLE_NAME,

        )



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



            logger.info(

                "INSERT BATCH START=%s END=%s SIZE=%s",

                start,

                end,

                len(batch),

            )



            self.clickhouse.insert(

                data=batch,

                columns=self.COLUMNS,

            )



            inserted += len(batch)



        logger.info(

            "INSERT COMPLETED TABLE=%s INSERTED=%s",

            self.TABLE_NAME,

            inserted,

        )



        logger.info(

            "STATUS: OK TABLE=%s",

            self.TABLE_NAME,

        )