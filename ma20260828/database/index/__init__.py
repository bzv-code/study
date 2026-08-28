from __future__ import annotations

from typing import Any

from client.moex_client import MoexClient
from models.candle_model import CandleModel
from services.security_service import SecurityService


class CandleService:

    def __init__(
        self,
        client: MoexClient,
        security_service: SecurityService,
    ) -> None:

        self.client = client
        self.security_service = security_service

    @staticmethod
    def _parse_table(
        response: dict[str, Any],
        table_name: str,
    ) -> list[dict[str, Any]]:
        """
        Преобразует таблицу ISS API в список словарей.
        """

        table = response.get(table_name)

        if table is None:
            return []

        columns = table.get("columns", [])
        rows = table.get("data", [])

        return [
            dict(zip(columns, row))
            for row in rows
        ]

    def get(
        self,
        secid: str,
        date_from: str,
        date_till: str,
        interval: int = 24,
    ) -> list[CandleModel]:
        """
        Возвращает список свечей.
        """

        security = self.security_service.get(secid)

        response = self.client.get_candles(
            engine=security.engine,
            market=security.market,
            security=secid,
            date_from=date_from,
            date_till=date_till,
            interval=interval,
        )

        candles = self._parse_table(
            response,
            "candles",
        )

        result: list[CandleModel] = []

        for candle in candles:

            result.append(
                CandleModel(
                    begin=candle.get("begin", ""),
                    end=candle.get("end", ""),
                    open=candle.get("open") or 0,
                    high=candle.get("high") or 0,
                    low=candle.get("low") or 0,
                    close=candle.get("close") or 0,
                    volume=candle.get("volume") or 0,
                    value=candle.get("value") or 0,
                )
            )

        return result