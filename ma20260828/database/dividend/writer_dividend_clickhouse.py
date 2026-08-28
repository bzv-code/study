from __future__ import annotations


from typing import Any


from models.dividend_model import DividendModel


from database.dividend.dividend_clickhouse import (
    DividendClickHouse,
)


from database.duplicate_checker_clickhouse import (
    DuplicateCheckerClickHouse,
)


from utils.logger import get_logger



logger = get_logger(__name__)







class DividendWriterClickHouse:
    """
    Загрузчик дивидендов акций MOEX
    в ClickHouse.


    Таблица:

        moex_api.moex_stock_dividends


    Источник:

        DividendModel


    Проверка дублей:

        secid + registry_close_date

    """



    TABLE_NAME = "moex_api.moex_stock_dividends"


    BATCH_SIZE = 5000







    COLUMNS = [

        "secid",

        "isin",

        "registry_close_date",

        "value",

        "currency",

    ]







    KEY_COLUMNS = [

        "secid",

        "registry_close_date",

    ]









    def __init__(
        self,
        clickhouse: DividendClickHouse,
    ) -> None:


        self.clickhouse = clickhouse



        self.duplicate_checker = DuplicateCheckerClickHouse(

            clickhouse.client

        )



        logger.debug(

            "DividendWriterClickHouse initialized TABLE=%s",

            self.TABLE_NAME,

        )









    def _prepare_row(
        self,
        dividend: DividendModel,
    ) -> list[Any]:
        """
        DividendModel
        -> строка ClickHouse.
        """


        logger.debug(

            "PREPARE DIVIDEND ROW SECID=%s DATE=%s",

            dividend.secid,

            dividend.registry_close_date,

        )



        return [

            dividend.secid,

            dividend.isin,

            dividend.registry_close_date,

            dividend.value,

            dividend.currency,

        ]









    def write(
        self,
        dividends: list[DividendModel],
    ) -> None:
        """
        Запись дивидендов
        чанками в ClickHouse.
        """


        if not dividends:


            logger.warning(

                "NO DIVIDENDS FOR INSERT TABLE=%s",

                self.TABLE_NAME,

            )



            print(

                "NO DATA FOR INSERT"

            )



            return









        logger.info(

            "CLICKHOUSE DIVIDEND INSERT START TABLE=%s INPUT=%s",

            self.TABLE_NAME,

            len(dividends),

        )





        print("=" * 80)

        print(
            "CLICKHOUSE INSERT DIVIDENDS"
        )

        print("=" * 80)







        rows = [

            self._prepare_row(

                dividend

            )

            for dividend in dividends

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

                    "CLICKHOUSE DIVIDEND INSERT ERROR TABLE=%s ERROR=%s",

                    self.TABLE_NAME,

                    error,

                )



                raise









            inserted += len(batch)









        logger.info(

            "CLICKHOUSE DIVIDEND INSERT COMPLETE TABLE=%s INSERTED=%s",

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