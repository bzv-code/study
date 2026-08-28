from __future__ import annotations


from typing import Any


import clickhouse_connect


from database.config_clickhouse import ClickHouseConfig

from utils.logger import get_logger



logger = get_logger(__name__)





class ClickHouseClient:
    """
    Универсальный клиент ClickHouse.

    Отвечает за:

    - подключение к ClickHouse
    - выполнение SQL команд
    - выполнение SELECT запросов
    - пакетную вставку данных

    Используется всеми разделами:

    metal
    currency
    stocks
    futures
    dividends
    """





    def __init__(
        self,
    ) -> None:



        logger.info(

            "CLICKHOUSE CONNECT START HOST=%s PORT=%s DATABASE=%s",

            ClickHouseConfig.HOST,

            ClickHouseConfig.PORT,

            ClickHouseConfig.DATABASE,

        )



        try:



            self.client = clickhouse_connect.get_client(



                host=ClickHouseConfig.HOST,



                port=ClickHouseConfig.PORT,



                username=ClickHouseConfig.USER,



                password=ClickHouseConfig.PASSWORD,



                database=ClickHouseConfig.DATABASE,



            )



            logger.info(

                "CLICKHOUSE CONNECTED DATABASE=%s",

                ClickHouseConfig.DATABASE,

            )



        except Exception as error:



            logger.exception(

                "CLICKHOUSE CONNECTION ERROR: %s",

                error,

            )



            raise





        print(
            "CLICKHOUSE CONNECTED"
        )



        print(
            f"DATABASE: {ClickHouseConfig.DATABASE}"
        )







    # ------------------------------------------------------
    # SQL command
    # ------------------------------------------------------

    def execute(
        self,
        sql: str,
    ) -> Any:
        """
        Выполнение SQL команды.

        Используется для:

        CREATE DATABASE
        CREATE TABLE
        ALTER
        OPTIMIZE
        DROP
        """



        logger.debug(

            "CLICKHOUSE EXECUTE SQL=%s",

            sql,

        )



        try:



            result = self.client.command(



                sql



            )



            logger.debug(

                "CLICKHOUSE EXECUTE COMPLETE",

            )



            return result





        except Exception as error:



            logger.exception(

                "CLICKHOUSE EXECUTE ERROR SQL=%s ERROR=%s",

                sql,

                error,

            )



            raise







    # ------------------------------------------------------
    # Insert
    # ------------------------------------------------------

    def insert(
        self,
        table: str,
        data: list[list[Any]] | list[tuple[Any, ...]],
        columns: list[str],
    ) -> None:
        """
        Пакетная вставка данных.

        Используется Writer'ами.
        """



        logger.info(

            "CLICKHOUSE INSERT TABLE=%s ROWS=%s",

            table,

            len(data),

        )



        logger.debug(

            "CLICKHOUSE INSERT COLUMNS=%s",

            columns,

        )





        try:



            self.client.insert(



                table=table,



                data=data,



                column_names=columns,



            )



            logger.info(

                "CLICKHOUSE INSERT COMPLETE TABLE=%s ROWS=%s",

                table,

                len(data),

            )





        except Exception as error:



            logger.exception(

                "CLICKHOUSE INSERT ERROR TABLE=%s ERROR=%s",

                table,

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
        SELECT запрос.

        Возвращает QueryResult.
        """



        logger.debug(

            "CLICKHOUSE QUERY SQL=%s",

            sql,

        )



        try:



            result = self.client.query(



                sql



            )



            logger.debug(

                "CLICKHOUSE QUERY COMPLETE",

            )



            return result





        except Exception as error:



            logger.exception(

                "CLICKHOUSE QUERY ERROR SQL=%s ERROR=%s",

                sql,

                error,

            )



            raise







    # ------------------------------------------------------
    # Ping
    # ------------------------------------------------------

    def ping(
        self,
    ) -> bool:
        """
        Проверка подключения.
        """



        logger.debug(

            "CLICKHOUSE PING START",

        )



        try:



            self.client.command(



                "SELECT 1"



            )



            logger.debug(

                "CLICKHOUSE PING OK",

            )



            return True





        except Exception as error:



            logger.error(

                "CLICKHOUSE PING FAILED ERROR=%s",

                error,

            )



            return False







    # ------------------------------------------------------
    # Close
    # ------------------------------------------------------

    def close(
        self,
    ) -> None:
        """
        Закрытие соединения.
        """



        if self.client is not None:



            try:



                self.client.close()



                logger.info(

                    "CLICKHOUSE CONNECTION CLOSED",

                )



                print(
                    "CLICKHOUSE CONNECTION CLOSED"
                )





            except Exception as error:



                logger.exception(

                    "CLICKHOUSE CLOSE ERROR=%s",

                    error,

                )







    # ------------------------------------------------------
    # Context manager
    # ------------------------------------------------------

    def __enter__(
        self,
    ) -> "ClickHouseClient":


        logger.debug(

            "CLICKHOUSE CONTEXT ENTER",

        )


        return self





    def __exit__(
        self,
        exc_type,
        exc_val,
        exc_tb,
    ) -> None:


        logger.debug(

            "CLICKHOUSE CONTEXT EXIT",

        )


        self.close()