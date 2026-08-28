# ma20260826/services/stock_foreign_service.py
from __future__ import annotations

from client.moex_client import MoexClient
from models.stock_model import StockModel
from utils.logger import get_logger

logger = get_logger(__name__)


class StockForeignService:
    """
    Сервис для получения списка и метаданных зарубежных акций на MOEX.
    Зарубежные акции обращаются на движке 'otc', рынке 'shares'.
    """

    def __init__(self, client: MoexClient) -> None:
        self.client = client
        self.engine = "otc"
        self.market = "shares"
        self._cache: list[StockModel] | None = None

    def get_all(self) -> list[StockModel]:
        """
        Возвращает список всех торгуемых зарубежных акций.
        Фильтр: ISIN не начинается с 'RU' и тикер заканчивается на '-RM'.
        """
        if self._cache is not None:
            return self._cache

        logger.info("Fetching foreign stocks from MOEX OTC market...")
        response = self.client.get(
            f"engines/{self.engine}/markets/{self.market}/securities.json",
            params={"limit": 1000}
        )

        securities = response.get("securities", {}).get("data", [])
        columns = response.get("securities", {}).get("columns", [])
        col_idx = {col: idx for idx, col in enumerate(columns)}

        result = []
        for row in securities:
            secid = row[col_idx.get("SECID", 0)]
            isin = row[col_idx.get("ISIN", 0)]
            shortname = row[col_idx.get("SHORTNAME", 0)]
            board = row[col_idx.get("BOARDID", 0)]

            # Фильтр: только бумаги с зарубежным ISIN и суффиксом -RM
            if isinstance(secid, str) and secid.endswith("-RM"):
                if isinstance(isin, str) and not isin.startswith("RU"):
                    result.append(
                        StockModel(
                            secid=secid,
                            shortname=shortname,
                            engine=self.engine,
                            market=self.market,
                            board=board or "MTQR",
                            isin=isin,
                        )
                    )

        self._cache = result
        logger.info(f"Found {len(result)} foreign stocks.")
        return result

    def get_by_secid(self, secid: str) -> StockModel | None:
        """Поиск конкретной акции по тикеру."""
        for stock in self.get_all():
            if stock.secid.upper() == secid.upper():
                return stock
        return None