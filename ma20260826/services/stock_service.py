from __future__ import annotations

from catalog.stock_catalog import StockCatalog

from models.stock_model import StockModel

from utils.logger import get_logger


logger = get_logger(__name__)


class StockService:
    """
    Сервис работы с акциями MOEX.

    Отвечает только за бизнес-логику.

    Источник данных:

        StockCatalog
    """

    def __init__(
        self,
        catalog: StockCatalog,
    ) -> None:

        self.catalog = catalog

        logger.debug(
            "StockService initialized"
        )

    def get(
        self,
        secid: str,
    ) -> StockModel:
        """
        Получить основной вариант акции.
        """

        logger.debug(
            "GET STOCK SECID=%s",
            secid,
        )

        if not secid:

            logger.warning(
                "GET STOCK WITHOUT SECID"
            )

            raise ValueError(
                "SECID не указан"
            )

        stock = self.catalog.get(
            secid.upper()
        )

        logger.info(
            "STOCK FOUND SECID=%s",
            secid.upper(),
        )

        return stock

    def get_all(
        self,
        secid: str,
    ) -> list[StockModel]:
        """
        Получить все варианты акции.

        Например:

            GAZP

        Вернет:

            TQBR
            SMAL
            SPEQ
        """

        logger.debug(
            "GET ALL STOCKS SECID=%s",
            secid,
        )

        if not secid:

            logger.warning(
                "GET ALL STOCKS WITHOUT SECID"
            )

            return []

        stocks = self.catalog.get_all(
            secid.upper()
        )

        logger.debug(
            "STOCK VARIANTS FOUND SECID=%s COUNT=%s",
            secid.upper(),
            len(stocks),
        )

        if stocks:

            logger.debug(
                "STOCK BOARDS SECID=%s BOARDS=%s",
                secid.upper(),
                [
                    item.board
                    for item in stocks
                ],
            )

        return stocks

    def exists(
        self,
        secid: str,
    ) -> bool:
        """
        Проверяет наличие акции
        в каталоге.
        """

        logger.debug(
            "CHECK STOCK EXISTS SECID=%s",
            secid,
        )

        if not secid:

            logger.warning(
                "CHECK STOCK EXISTS WITHOUT SECID"
            )

            return False

        result = self.catalog.exists(
            secid.upper()
        )

        logger.debug(
            "STOCK EXISTS SECID=%s RESULT=%s",
            secid.upper(),
            result,
        )

        return result

    def search(
        self,
        text: str,
    ) -> list[StockModel]:
        """
        Поиск акции по SECID
        и названию.
        """

        logger.debug(
            "SEARCH STOCK TEXT=%s",
            text,
        )

        if not text:

            logger.warning(
                "SEARCH STOCK WITHOUT TEXT"
            )

            return []

        result = self.catalog.search(
            text
        )

        logger.debug(
            "SEARCH STOCK RESULT TEXT=%s COUNT=%s",
            text,
            len(result),
        )

        return result

    def get_primary(
        self,
        secid: str,
    ) -> StockModel:
        """
        Получить основной вариант акции.

        Алиас для get().

        Используется
        StockCandleService.
        """

        logger.debug(
            "GET PRIMARY STOCK SECID=%s",
            secid,
        )

        return self.get(
            secid
        )