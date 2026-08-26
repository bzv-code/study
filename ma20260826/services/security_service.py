from __future__ import annotations


from catalog.instrument_catalog import InstrumentCatalog

from models.security_model import SecurityModel

from utils.logger import get_logger



logger = get_logger(__name__)




class SecurityService:
    """
    Сервис работы с инструментами MOEX.

    Отвечает только за бизнес-слой.
    Источник данных:
    InstrumentCatalog.
    """



    def __init__(
        self,
        catalog: InstrumentCatalog,
    ) -> None:

        self.catalog = catalog


        logger.debug(
            "SecurityService initialized"
        )





    def get(
        self,
        secid: str,
    ) -> SecurityModel:
        """
        Получить основной вариант инструмента.
        """

        logger.debug(
            "GET SECURITY SECID=%s",
            secid,
        )


        if not secid:

            logger.warning(
                "GET SECURITY WITHOUT SECID"
            )

            raise ValueError(
                "SECID не указан"
            )



        security = self.catalog.get(
            secid.upper()
        )


        logger.info(
            "SECURITY FOUND SECID=%s",
            secid.upper(),
        )


        return security





    def get_all(
        self,
        secid: str,
    ) -> list[SecurityModel]:
        """
        Получить все варианты инструмента.

        Например:

        GLDRUB_TOM

        CETS
        CNGD
        LICU
        """


        logger.debug(
            "GET ALL SECURITIES SECID=%s",
            secid,
        )


        if not secid:

            logger.warning(
                "GET ALL WITHOUT SECID"
            )

            return []



        securities = self.catalog.get_all(
            secid.upper()
        )


        logger.debug(
            "SECURITY VARIANTS FOUND SECID=%s COUNT=%s",
            secid.upper(),
            len(securities),
        )


        if securities:

            logger.debug(
                "SECURITY BOARDS SECID=%s BOARDS=%s",
                secid.upper(),
                [
                    item.board
                    for item in securities
                ],
            )


        return securities





    def exists(
        self,
        secid: str,
    ) -> bool:
        """
        Проверяет наличие инструмента
        в каталоге.
        """


        logger.debug(
            "CHECK SECURITY EXISTS SECID=%s",
            secid,
        )


        if not secid:

            logger.warning(
                "CHECK EXISTS WITHOUT SECID"
            )

            return False



        result = self.catalog.exists(
            secid.upper()
        )


        logger.debug(
            "SECURITY EXISTS SECID=%s RESULT=%s",
            secid.upper(),
            result,
        )


        return result





    def search(
        self,
        text: str,
    ) -> list[SecurityModel]:
        """
        Поиск по SECID и названию.
        """


        logger.debug(
            "SEARCH SECURITY TEXT=%s",
            text,
        )


        if not text:

            logger.warning(
                "SEARCH WITHOUT TEXT"
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





    def get_primary(
        self,
        secid: str,
    ) -> SecurityModel:
        """
        Получить лучший вариант площадки.

        Алиас для get().
        Используется в свечах.
        """


        logger.debug(
            "GET PRIMARY SECURITY SECID=%s",
            secid,
        )


        return self.get(
            secid
        )