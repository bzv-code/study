from __future__ import annotations


from datetime import datetime

from typing import Any



from models.metal_model import MetalModel


from database.metal.metal_clickhouse import MetalClickHouse

from database.duplicate_checker_clickhouse import DuplicateCheckerClickHouse


from utils.datetime_utils import parse_moscow_datetime

from utils.logger import get_logger



logger = get_logger(__name__)





class MetalH1WriterClickHouse:
    """
    Загрузчик часовых свечей металлов MOEX
    в ClickHouse.


    Таблица:

        moex_api.moex_metal_h1


    Таймфрейм:

        1 час


    Проверка дублей:

        ticker + date

    """



    TABLE_NAME = "moex_api.moex_metal_h1"



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

            "MetalH1WriterClickHouse initialized TABLE=%s",

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


        logger.debug(

            "PREPARE ROW TICKER=%s DATE=%s",

            item.ticker,

            item.date,

        )


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
        Запись часовых свечей чанками.


        Перед вставкой:

        - подготовка даты MOEX;
        - проверка существующих записей;
        - удаление дублей внутри пакета;
        - пакетная вставка.

        """



        if not metals:


            logger.warning(

                "NO DATA FOR INSERT TABLE=%s",

                self.TABLE_NAME,

            )


            print(

                "NO DATA FOR INSERT"

            )


            return





        logger.info(

            "CLICKHOUSE INSERT START TABLE=%s INPUT_ROWS=%s",

            self.TABLE_NAME,

            len(metals),

        )





        print("=" * 80)

        print(

            "CLICKHOUSE INSERT METAL H1"

        )

        print("=" * 80)





        rows = [

            self._prepare_row(

                item

            )

            for item in metals

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







        logger.info(

            "ROWS AFTER DUPLICATE CHECK COUNT=%s",

            len(rows),

        )







        if not rows:


            logger.info(

                "NOTHING TO INSERT TABLE=%s",

                self.TABLE_NAME,

            )


            print(

                "NOTHING TO INSERT"

            )


            return






        print(

            f"READY INSERT: {len(rows)}"

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

                    "CLICKHOUSE INSERT ERROR TABLE=%s ERROR=%s",

                    self.TABLE_NAME,

                    error,

                )


                raise





            inserted += len(batch)







        logger.info(

            "CLICKHOUSE INSERT COMPLETE TABLE=%s INSERTED=%s",

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