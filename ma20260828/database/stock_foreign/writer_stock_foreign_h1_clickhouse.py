# moex_api/database/stock_foreign/writer_stock_foreign_h1_clickhouse.py
from __future__ import annotations

from datetime import datetime
from typing import Any

from models.stock_model import StockModel
from models.candle_model import CandleModel

from database.stock_foreign.stock_foreign_clickhouse import StockForeignClickHouse
from database.duplicate_checker_clickhouse import DuplicateCheckerClickHouse

from utils.datetime_utils import parse_moscow_datetime
from utils.logger import get_logger

logger = get_logger(__name__)


class StockForeignH1WriterClickHouse:
    """
    Загрузчик часовых свечей зарубежных акций MOEX в ClickHouse.

    Таблица:
        moex_api.moex_stock_foreign_h1

    Проверка дублей:
        secid + date
    """

    TABLE_NAME = "moex_api.moex_stock_foreign_h1"
    BATCH_SIZE = 5000

    COLUMNS = [
        "secid",
        "isin",
        "shortname",
        "sector",
        "country",
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

    def __init__(self, clickhouse: StockForeignClickHouse) -> None:
        self.clickhouse = clickhouse
        self.duplicate_checker = DuplicateCheckerClickHouse(clickhouse.client)
        logger.debug("StockForeignH1WriterClickHouse initialized TABLE=%s", self.TABLE_NAME)

    @staticmethod
    def _parse_date(value: datetime) -> datetime:
        """Приведение даты MOEX к Europe/Moscow."""
        return parse_moscow_datetime(value)

    def _prepare_row(
            self,
            stock: StockModel,
            candle: CandleModel,
            country: str,
            sector: str,
    ) -> list[Any]:
        """
        StockModel + CandleModel + country + sector -> строка ClickHouse.
        """
        logger.debug("PREPARE STOCK FOREIGN H1 ROW SECID=%s DATE=%s", stock.secid, candle.begin)

        return [
            stock.secid,
            getattr(stock, 'isin', 'N/A'),
            stock.shortname,
            sector,
            country,
            stock.engine,
            stock.market,
            stock.board,
            self._parse_date(candle.begin),
            float(candle.open),
            float(candle.high),
            float(candle.low),
            float(candle.close),
            int(candle.volume),
            float(candle.value),
        ]

    def write(
            self,
            stock: StockModel,
            candles: list[CandleModel],
            country: str,
            sector: str,
    ) -> None:
        """Запись часовых свечей зарубежных акций чанками в ClickHouse."""
        if not candles:
            logger.warning("NO CANDLES FOR INSERT TABLE=%s", self.TABLE_NAME)
            print("NO DATA FOR INSERT")
            return

        logger.info("CLICKHOUSE STOCK FOREIGN H1 INSERT START TABLE=%s INPUT=%s", self.TABLE_NAME, len(candles))
        print("=" * 80)
        print("CLICKHOUSE INSERT STOCK FOREIGN H1")
        print("=" * 80)

        rows = [
            self._prepare_row(stock, candle, country, sector)
            for candle in candles
        ]

        logger.debug("ROWS PREPARED COUNT=%s", len(rows))
        print(f"INPUT ROWS: {len(rows)}")

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

        logger.info("ROWS AFTER DUPLICATE CHECK COUNT=%s", len(rows))

        if not rows:
            print("NOTHING TO INSERT")
            return

        inserted = 0

        for start in range(0, len(rows), self.BATCH_SIZE):
            end = min(start + self.BATCH_SIZE, len(rows))
            batch = rows[start:end]

            logger.debug("INSERT BATCH START=%s END=%s SIZE=%s", start, end, len(batch))
            print(f"INSERT BATCH: {start} - {end}")

            try:
                self.clickhouse.insert(data=batch, columns=self.COLUMNS)
            except Exception as error:
                logger.exception("CLICKHOUSE STOCK FOREIGN H1 INSERT ERROR TABLE=%s ERROR=%s", self.TABLE_NAME, error)
                raise

            inserted += len(batch)

        logger.info("CLICKHOUSE STOCK FOREIGN H1 INSERT COMPLETE TABLE=%s INSERTED=%s", self.TABLE_NAME, inserted)
        print()
        print(f"INSERTED: {inserted}")
        print("STATUS: OK")
        print("=" * 80)