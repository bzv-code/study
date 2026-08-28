from __future__ import annotations

from catalog.futures_catalog import FuturesCatalog
from models.futures_model import FuturesModel
from utils.logger import get_logger


logger = get_logger(__name__)


class FuturesService:
    """
    Сервис работы с фьючерсами MOEX.

    Отвечает только за бизнес-логику.

    Источник данных:

        FuturesCatalog
    """

    def __init__(
        self,
        catalog: FuturesCatalog,
    ) -> None:

        self.catalog = catalog

        logger.debug(
            "FuturesService initialized"
        )

    # ==================================================
    # SECID
    # ==================================================

    def get(
        self,
        secid: str,
    ) -> FuturesModel:
        """
        Получить контракт по точному SECID.

        Например:

            SiU6
            BRZ6
            GZU6
        """

        logger.debug(
            "GET FUTURES SECID=%s",
            secid,
        )

        if not secid:

            logger.warning(
                "GET FUTURES WITHOUT SECID"
            )

            raise ValueError(
                "SECID не указан"
            )

        future = self.catalog.get(
            secid.upper()
        )

        logger.info(
            "FUTURES FOUND SECID=%s",
            future.secid,
        )

        return future

    def exists(
        self,
        secid: str,
    ) -> bool:
        """
        Проверить наличие контракта.
        """

        logger.debug(
            "CHECK FUTURES EXISTS SECID=%s",
            secid,
        )

        if not secid:
            return False

        result = self.catalog.exists(
            secid.upper()
        )

        logger.debug(
            "FUTURES EXISTS=%s",
            result,
        )

        return result

    # ==================================================
    # Asset
    # ==================================================

    def get_all(
        self,
        asset_code: str,
    ) -> list[FuturesModel]:
        """
        Получить все контракты базового актива.

        Например:

            BR

        Вернет:

            BRU6
            BRZ6
            BRH7
            BRM7
            ...

        Или

            GAZR

        Вернет:

            GZU6
            GZZ6
            GZH7
            GZM7
        """

        logger.debug(
            "GET FUTURES BY ASSET=%s",
            asset_code,
        )

        if not asset_code:

            logger.warning(
                "GET FUTURES WITHOUT ASSET"
            )

            return []

        futures = self.catalog.search(
            asset_code
        )

        asset_code = asset_code.upper()

        futures = [
            item
            for item in futures
            if item.asset_code.upper() == asset_code
        ]

        futures.sort(
            key=lambda x:
            x.last_delivery_date
            or x.last_trade_date
        )

        logger.debug(
            "FOUND FUTURES ASSET=%s COUNT=%s",
            asset_code,
            len(futures),
        )

        return futures

    def by_asset(
        self,
        asset_code: str,
    ) -> list[FuturesModel]:
        """
        Алиас get_all().
        """

        return self.get_all(
            asset_code
        )

    def search_by_asset(
        self,
        asset_code: str,
    ) -> list[FuturesModel]:
        """
        Поиск по asset_code.

        Полный синоним by_asset().
        """

        return self.by_asset(
            asset_code
        )

    def get_nearest(
        self,
        asset_code: str,
    ) -> FuturesModel | None:
        """
        Получить ближайший контракт.

        Например:

            BR

        -> BRU6
        """

        logger.debug(
            "GET NEAREST FUTURES ASSET=%s",
            asset_code,
        )

        futures = self.get_all(
            asset_code
        )

        if not futures:

            logger.warning(
                "NO FUTURES FOR ASSET=%s",
                asset_code,
            )

            return None

        nearest = futures[0]

        logger.info(
            "NEAREST FUTURES SECID=%s DELIVERY=%s",
            nearest.secid,
            nearest.last_delivery_date,
        )

        return nearest

    # ==================================================
    # Search
    # ==================================================

    def search(
        self,
        text: str,
    ) -> list[FuturesModel]:
        """
        Полнотекстовый поиск.

        Поиск производится по:

            SECID
            asset_code
            shortname
            secname
        """

        logger.debug(
            "SEARCH FUTURES TEXT=%s",
            text,
        )

        if not text:

            logger.warning(
                "SEARCH FUTURES WITHOUT TEXT"
            )

            return []

        result = self.catalog.search(
            text
        )

        logger.debug(
            "SEARCH RESULT TEXT=%s COUNT=%s",
            text,
            len(result),
        )

        return result

    # ==================================================
    # Compatibility
    # ==================================================

    def get_primary(
        self,
        secid: str,
    ) -> FuturesModel:
        """
        Алиас get().
        """

        logger.debug(
            "GET PRIMARY FUTURES SECID=%s",
            secid,
        )

        return self.get(
            secid
        )