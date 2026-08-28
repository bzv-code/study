from __future__ import annotations


from collections import defaultdict
from typing import Final


import httpx


from client.moex_client import MoexClient

from models.security_model import SecurityModel

from utils.iss_parser import IssParser

from utils.logger import get_logger



logger = get_logger(__name__)




BOARD_PRIORITY: Final[dict[str, int]] = {

    # металлы - тестируем CETS
    "CETS": 100,

    # специальные котировки металлов
    "LICU": 90,

    "CNGD": 80,

    "TQBR": 70,

    "TQOB": 60,

    "RFUD": 50,

}




class InstrumentCatalog:
    """
    Быстрый каталог инструментов MOEX.

    Не загружает весь рынок.
    Ищет только необходимые SECID.
    """


    SEARCH_MARKETS = [

        (
            "currency",
            "selt",
        ),

    ]


    LOAD_LIMIT = 5000





    def __init__(
        self,
        client: MoexClient,
    ) -> None:


        self.client = client


        self._items: dict[
            str,
            list[SecurityModel],
        ] = defaultdict(list)



        self._loaded_markets: set[
            tuple[str, str]
        ] = set()



        logger.debug(
            "InstrumentCatalog initialized"
        )




    # ==================================================
    # Загрузка рынка
    # ==================================================

    def load_market(
        self,
        engine: str,
        market: str,
    ) -> None:


        key = (
            engine,
            market,
        )


        if key in self._loaded_markets:


            logger.debug(
                "MARKET ALREADY LOADED %s/%s",
                engine,
                market,
            )


            return





        logger.info(
            "LOAD MARKET %s/%s",
            engine,
            market,
        )



        try:

            response = self.client.get_market_securities(

                engine,

                market,

                start=0,

                limit=self.LOAD_LIMIT,

            )


        except httpx.HTTPError as error:


            logger.exception(
                "LOAD MARKET ERROR %s/%s ERROR=%s",
                engine,
                market,
                error,
            )


            return





        rows = IssParser.table(

            response,

            "securities",

        )




        logger.info(
            "MARKET LOADED %s/%s INSTRUMENTS=%s",
            engine,
            market,
            len(rows),
        )




        for row in rows:


            self._add(

                row,

                engine,

                market,

            )




        self._loaded_markets.add(
            key
        )




        logger.debug(
            "MARKET CACHE UPDATED %s/%s TOTAL=%s",
            engine,
            market,
            self.count(),
        )





    # ==================================================
    # Добавление
    # ==================================================

    def _add(
        self,
        row: dict,
        engine: str,
        market: str,
    ) -> None:


        secid = row.get(
            "SECID"
        )


        if not secid:


            logger.debug(
                "SKIP SECURITY WITHOUT SECID"
            )


            return





        security = SecurityModel(


            secid=secid,



            shortname=row.get(

                "SHORTNAME",

                "",

            ),



            engine=engine,



            market=market,



            board=row.get(

                "BOARDID",

                "",

            ),



            isin=row.get(

                "ISIN",

                "",

            ),



            currency=row.get(

                "FACEUNIT",

                "",

            ),



            decimals=int(

                row.get(

                    "DECIMALS"

                )

                or 0

            ),



            lotsize=int(

                row.get(

                    "LOTSIZE"

                )

                or 0

            ),


        )





        exists = any(

            x.engine == security.engine

            and x.market == security.market

            and x.board == security.board


            for x in self._items[secid]

        )





        if not exists:


            self._items[secid].append(

                security

            )


            logger.debug(

                "ADD SECURITY SECID=%s BOARD=%s MARKET=%s",

                security.secid,

                security.board,

                security.market,

            )






    # ==================================================
    # Металлы
    # ==================================================

    def load_metals(
        self,
    ) -> None:


        logger.debug(
            "LOAD METALS MARKETS"
        )



        for engine, market in self.SEARCH_MARKETS:


            self.load_market(

                engine,

                market,

            )





    # ==================================================
    # API
    # ==================================================

    def get_all(
        self,
        secid: str,
    ) -> list[SecurityModel]:


        secid = secid.upper()



        logger.debug(
            "GET ALL SECURITIES SECID=%s",
            secid,
        )



        result = self._items.get(

            secid,

            [],

        )



        if result:


            logger.debug(

                "SECURITY FOUND IN CACHE SECID=%s COUNT=%s",

                secid,

                len(result),

            )


            return result





        logger.debug(

            "SECURITY NOT FOUND CACHE LOAD MARKETS SECID=%s",

            secid,

        )



        self.load_metals()



        result = self._items.get(

            secid,

            [],

        )



        logger.debug(

            "SECURITY AFTER LOAD SECID=%s COUNT=%s",

            secid,

            len(result),

        )



        return result






    def get(
        self,
        secid: str,
    ) -> SecurityModel:


        secid = secid.upper()



        logger.debug(

            "GET PRIMARY SECURITY SECID=%s",

            secid,

        )



        variants = self.get_all(

            secid

        )





        if not variants:


            logger.debug(

                "SECOND LOAD TRY SECID=%s",

                secid,

            )


            self.load_metals()



            variants = self.get_all(

                secid

            )





        if not variants:


            logger.error(

                "SECURITY NOT FOUND SECID=%s",

                secid,

            )


            raise ValueError(

                f"Инструмент '{secid}' не найден"

            )





        selected = max(

            variants,


            key=lambda x:


            BOARD_PRIORITY.get(

                x.board,

                0,

            ),


        )





        logger.info(

            "PRIMARY SECURITY SELECTED SECID=%s BOARD=%s",

            secid,

            selected.board,

        )



        return selected





    def exists(
        self,
        secid: str,
    ) -> bool:


        result = bool(

            self.get_all(secid)

        )



        logger.debug(

            "CHECK SECURITY EXISTS SECID=%s RESULT=%s",

            secid,

            result,

        )


        return result





    def count(
        self,
    ) -> int:


        total = sum(

            len(items)

            for items in self._items.values()

        )



        logger.debug(

            "CATALOG COUNT=%s",

            total,

        )



        return total