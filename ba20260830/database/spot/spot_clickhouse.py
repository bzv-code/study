from __future__ import annotations

from typing import Any

from database.client_clickhouse import ClickHouseClient

# Если у вас есть utils.logger, оставьте этот импорт.
# Если нет, замените на стандартный: import logging; logger = logging.getLogger(__name__)
try:
    from utils.logger import get_logger

    logger = get_logger(__name__)
except ImportError:
    import logging

    logger = logging.getLogger(__name__)


class BybitSpotClickHouse:
    """
    Универсальный репозиторий ClickHouse
    для данных спотового рынка Bybit.

    Поддерживает таблицы, например:
        bybit_spot.candles_d (дневные свечи)
        bybit_spot.candles_1h (часовые свечи)

    Отвечает только за работу с таблицами Bybit Spot.

    Управление подключением:
        database.client_clickhouse.ClickHouseClient
    """

    DATABASE = "bybit_spot"

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
            "BybitSpotClickHouse initialized TABLE=%s",
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
        Вставка данных в ClickHouse.
        """
        logger.info(
            "CLICKHOUSE BYBIT_SPOT INSERT TABLE=%s ROWS=%s",
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
                "CLICKHOUSE BYBIT_SPOT INSERT COMPLETE TABLE=%s ROWS=%s",
                self.table_name,
                len(data),
            )

        except Exception as error:
            logger.exception(
                "CLICKHOUSE BYBIT_SPOT INSERT ERROR TABLE=%s ERROR=%s",
                self.table_name,
                error,
            )
            raise

    # ------------------------------------------------------
    # Query
    # ------------------------------------------------------
    def query(self, sql: str, parameters: dict | None = None):
        """
        SELECT запрос.
        """
        logger.debug(
            "CLICKHOUSE BYBIT_SPOT QUERY TABLE=%s SQL=%s",
            self.table_name,
            sql,
        )

        try:
            result = self.client.query(sql, parameters=parameters)

            logger.debug(
                "CLICKHOUSE BYBIT_SPOT QUERY COMPLETE TABLE=%s",
                self.table_name,
            )
            return result

        except Exception as error:
            logger.exception(
                "CLICKHOUSE BYBIT_SPOT QUERY ERROR TABLE=%s ERROR=%s",
                self.table_name,
                error,
            )
            raise

    # ------------------------------------------------------
    # Execute
    # ------------------------------------------------------
    def execute(self, sql: str) -> Any:
        """
        Выполнение SQL команд (CREATE, ALTER и т.д.).
        """
        logger.debug(
            "CLICKHOUSE BYBIT_SPOT EXECUTE TABLE=%s SQL=%s",
            self.table_name,
            sql,
        )

        try:
            result = self.client.execute(sql)

            logger.debug(
                "CLICKHOUSE BYBIT_SPOT EXECUTE COMPLETE TABLE=%s",
                self.table_name,
            )
            return result

        except Exception as error:
            logger.exception(
                "CLICKHOUSE BYBIT_SPOT EXECUTE ERROR TABLE=%s ERROR=%s",
                self.table_name,
                error,
            )
            raise

    # ------------------------------------------------------
    # Table name
    # ------------------------------------------------------
    def get_table_name(self) -> str:
        """
        Получить полное имя таблицы.
        """
        logger.debug("GET BYBIT_SPOT TABLE NAME=%s", self.table_name)
        return self.table_name