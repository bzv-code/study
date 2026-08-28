# moex_api/database/stock_foreign/stock_foreign_clickhouse.py
from __future__ import annotations

from typing import Any
from database.client_clickhouse import ClickHouseClient
from utils.logger import get_logger

logger = get_logger(__name__)


class StockForeignClickHouse:
    """
    Универсальный репозиторий ClickHouse
    для данных зарубежных акций MOEX.

    Поддерживает таблицы:
        moex_api.moex_stock_foreign_d

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
            table_name if "." in table_name else f"{self.DATABASE}.{table_name}"
        )

        logger.debug("StockForeignClickHouse initialized TABLE=%s", self.table_name)

    # ------------------------------------------------------
    # Insert
    # ------------------------------------------------------
    def insert(self, data: list[list[Any]], columns: list[str]) -> None:
        """Вставка данных в ClickHouse."""
        logger.info("CLICKHOUSE INSERT STOCK FOREIGN TABLE=%s ROWS=%s", self.table_name, len(data))
        logger.debug("INSERT COLUMNS=%s", columns)

        try:
            self.client.insert(table=self.table_name, data=data, columns=columns)
            logger.info("CLICKHOUSE STOCK FOREIGN INSERT COMPLETE TABLE=%s ROWS=%s", self.table_name, len(data))
        except Exception as error:
            logger.exception("CLICKHOUSE STOCK FOREIGN INSERT ERROR TABLE=%s ERROR=%s", self.table_name, error)
            raise

    # ------------------------------------------------------
    # Query
    # ------------------------------------------------------
    def query(self, sql: str):
        """SELECT запрос."""
        logger.debug("CLICKHOUSE STOCK FOREIGN QUERY TABLE=%s SQL=%s", self.table_name, sql)
        try:
            result = self.client.query(sql)
            logger.debug("CLICKHOUSE STOCK FOREIGN QUERY COMPLETE TABLE=%s", self.table_name)
            return result
        except Exception as error:
            logger.exception("CLICKHOUSE STOCK FOREIGN QUERY ERROR TABLE=%s ERROR=%s", self.table_name, error)
            raise

    # ------------------------------------------------------
    # Execute
    # ------------------------------------------------------
    def execute(self, sql: str) -> Any:
        """Выполнение SQL команд."""
        logger.debug("CLICKHOUSE STOCK FOREIGN EXECUTE TABLE=%s SQL=%s", self.table_name, sql)
        try:
            result = self.client.execute(sql)
            logger.debug("CLICKHOUSE STOCK FOREIGN EXECUTE COMPLETE TABLE=%s", self.table_name)
            return result
        except Exception as error:
            logger.exception("CLICKHOUSE STOCK FOREIGN EXECUTE ERROR TABLE=%s ERROR=%s", self.table_name, error)
            raise

    # ------------------------------------------------------
    # Delete
    # ------------------------------------------------------
    def delete(self, sql: str) -> Any:
        """DELETE / ALTER запросы."""
        logger.debug("CLICKHOUSE STOCK FOREIGN DELETE TABLE=%s SQL=%s", self.table_name, sql)
        try:
            result = self.client.execute(sql)
            logger.info("CLICKHOUSE STOCK FOREIGN DELETE COMPLETE TABLE=%s", self.table_name)
            return result
        except Exception as error:
            logger.exception("CLICKHOUSE STOCK FOREIGN DELETE ERROR TABLE=%s ERROR=%s", self.table_name, error)
            raise

    # ------------------------------------------------------
    # Table name
    # ------------------------------------------------------
    def get_table_name(self) -> str:
        """Получить полное имя таблицы."""
        logger.debug("GET STOCK FOREIGN TABLE NAME=%s", self.table_name)
        return self.table_name