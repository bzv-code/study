from __future__ import annotations


from typing import Any


from database.client_clickhouse import ClickHouseClient


from utils.logger import get_logger



logger = get_logger(__name__)





class DividendClickHouse:
    """
    Универсальный репозиторий ClickHouse
    для дивидендов акций MOEX.


    Поддерживает таблицу:


        moex_api.moex_stock_dividends


    Отвечает только за работу
    с таблицей дивидендов.


    Управление подключением:


        database.client_clickhouse.ClickHouseClient

    """



    DATABASE = "moex_api"





    def __init__(
        self,
        client: ClickHouseClient,
        table_name: str,
    ) -> None:


        self.client = client



        self.table_name = (

            table_name

            if "." in table_name

            else f"{self.DATABASE}.{table_name}"

        )



        logger.debug(

            "DividendClickHouse initialized TABLE=%s",

            self.table_name,

        )









    # ------------------------------------------------------
    # Insert
    # ------------------------------------------------------

    def insert(
        self,
        data: list[list[Any]],
        columns: list[str],
    ) -> None:
        """
        Вставка дивидендов в ClickHouse.
        """


        logger.info(

            "CLICKHOUSE INSERT DIVIDEND TABLE=%s ROWS=%s",

            self.table_name,

            len(data),

        )



        logger.debug(

            "INSERT COLUMNS=%s",

            columns,

        )



        try:


            self.client.insert(

                table=self.table_name,

                data=data,

                columns=columns,

            )



            logger.info(

                "CLICKHOUSE DIVIDEND INSERT COMPLETE TABLE=%s ROWS=%s",

                self.table_name,

                len(data),

            )



        except Exception as error:


            logger.exception(

                "CLICKHOUSE DIVIDEND INSERT ERROR TABLE=%s ERROR=%s",

                self.table_name,

                error,

            )


            raise









    # ------------------------------------------------------
    # Query
    # ------------------------------------------------------

    def query(
        self,
        sql: str,
    ):
        """
        SELECT запрос по дивидендам.
        """


        logger.debug(

            "CLICKHOUSE DIVIDEND QUERY TABLE=%s SQL=%s",

            self.table_name,

            sql,

        )



        try:


            result = self.client.query(

                sql

            )


            logger.debug(

                "CLICKHOUSE DIVIDEND QUERY COMPLETE TABLE=%s",

                self.table_name,

            )


            return result



        except Exception as error:


            logger.exception(

                "CLICKHOUSE DIVIDEND QUERY ERROR TABLE=%s ERROR=%s",

                self.table_name,

                error,

            )


            raise









    # ------------------------------------------------------
    # Execute
    # ------------------------------------------------------

    def execute(
        self,
        sql: str,
    ) -> Any:
        """
        Выполнение SQL команд.
        """


        logger.debug(

            "CLICKHOUSE DIVIDEND EXECUTE TABLE=%s SQL=%s",

            self.table_name,

            sql,

        )



        try:


            result = self.client.execute(

                sql

            )



            logger.debug(

                "CLICKHOUSE DIVIDEND EXECUTE COMPLETE TABLE=%s",

                self.table_name,

            )



            return result



        except Exception as error:


            logger.exception(

                "CLICKHOUSE DIVIDEND EXECUTE ERROR TABLE=%s ERROR=%s",

                self.table_name,

                error,

            )


            raise









    # ------------------------------------------------------
    # Delete
    # ------------------------------------------------------

    def delete(
        self,
        sql: str,
    ) -> Any:
        """
        DELETE / ALTER запросы.
        """


        logger.debug(

            "CLICKHOUSE DIVIDEND DELETE TABLE=%s SQL=%s",

            self.table_name,

            sql,

        )



        try:


            result = self.client.execute(

                sql

            )



            logger.info(

                "CLICKHOUSE DIVIDEND DELETE COMPLETE TABLE=%s",

                self.table_name,

            )



            return result



        except Exception as error:


            logger.exception(

                "CLICKHOUSE DIVIDEND DELETE ERROR TABLE=%s ERROR=%s",

                self.table_name,

                error,

            )


            raise









    # ------------------------------------------------------
    # Table name
    # ------------------------------------------------------

    def get_table_name(
        self,
    ) -> str:
        """
        Получить полное имя таблицы.
        """


        logger.debug(

            "GET DIVIDEND TABLE NAME=%s",

            self.table_name,

        )


        return self.table_name