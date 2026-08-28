# ma20260826/services/stock_foreign_candle_service.py
from __future__ import annotations

from typing import Any

from client.moex_client import MoexClient
from models.candle_model import CandleModel
from services.stock_foreign_service import StockForeignService
from utils.datetime_utils import parse_moscow_datetime
from utils.logger import get_logger

logger = get_logger(__name__)

class StockForeignCandleService:
    """
    Сервис получения свечей по зарубежным акциям MOEX.
    """
    PAGE_SIZE = 500

    def __init__(
            self,
            client: MoexClient,
            stock_foreign_service: StockForeignService,
    ) -> None:
        self.client = client
        self.stock_foreign_service = stock_foreign_service

    @staticmethod
    def _parse_table(response: dict[str, Any], table_name: str) -> list[dict[str, Any]]:
        table = response.get(table_name)
        if not table:
            return []
        columns = table.get("columns", [])
        rows = table.get("data", [])
        return [dict(zip(columns, row)) for row in rows]

    def get(
            self,
            secid: str,
            date_from: str,
            date_till: str,
            interval: int = 24,
    ) -> list[CandleModel]:
        """
        Загружает свечи для зарубежной акции.
        interval: 24 (дневные), 60 (часовые), 1 (минутные) и т.д.
        """
        stock = self.stock_foreign_service.get_by_secid(secid)
        if not stock:
            raise ValueError(f"Зарубежная акция '{secid}' не найдена в списке MOEX.")

        logger.info(f"Fetching candles for {secid} from {date_from} to {date_till}")

        result = []
        start = 0

        while True:
            response = self.client.get_candles(
                engine=stock.engine,
                market=stock.market,
                security=stock.secid,
                date_from=date_from,
                date_till=date_till,
                interval=interval,
                start=start,
            )

            candles = self._parse_table(response, "candles")
            if not candles:
                break

            for item in candles:
                begin = parse_moscow_datetime(item.get("begin"))
                if begin:
                    result.append(
                        CandleModel(
                            secid=stock.secid,
                            ticker=stock.secid,
                            name=stock.shortname,
                            engine=stock.engine,
                            market=stock.market,
                            board=stock.board,
                            begin=begin,
                            end=parse_moscow_datetime(item.get("end")),
                            open=float(item.get("open") or 0),
                            high=float(item.get("high") or 0),
                            low=float(item.get("low") or 0),
                            close=float(item.get("close") or 0),
                            volume=int(item.get("volume") or 0),
                            value=float(item.get("value") or 0),
                        )
                    )

            if len(candles) < self.PAGE_SIZE:
                break

            start += self.PAGE_SIZE

        result.sort(key=lambda x: x.begin)
        logger.info(f"Successfully loaded {len(result)} candles for {secid}")
        return result