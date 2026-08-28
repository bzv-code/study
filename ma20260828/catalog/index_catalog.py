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


    # Основная доска индексов
    "RTSI": 100,


    # Индикативные значения
    "INAV": 90,


    # Товарные индексы
    "AGRO": 80,


}







class IndexCatalog:
    """
    Каталог индексов MOEX.


    Возвращает SecurityModel,
    совместимый с CandleService.


    Загружает:

        stock / index


    После первой загрузки
    использует внутренний кэш.
    """



    SEARCH_MARKETS = [


        (

            "stock",

            "index",

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
            "IndexCatalog initialized"
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



        secid = str(

            row.get(

                "SECID",

                "",

            )

        ).upper()



        if not secid:


            logger.debug(

                "SKIP INDEX WITHOUT SECID"

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






        if exists:


            return







        self._items[secid].append(

            security

        )






        logger.debug(

            "ADD INDEX SECID=%s BOARD=%s MARKET=%s",

            security.secid,

            security.board,

            security.market,

        )









    # ==================================================
    # Индексы
    # ==================================================


    def load_indices(
        self,
    ) -> None:



        logger.debug(

            "LOAD INDEX MARKETS"

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

            "GET ALL INDEX SECID=%s",

            secid,

        )






        result = self._items.get(

            secid,

            [],

        )






        if result:


            logger.debug(

                "INDEX FOUND CACHE SECID=%s COUNT=%s",

                secid,

                len(result),

            )


            return result







        logger.debug(

            "INDEX NOT FOUND CACHE LOAD MARKET SECID=%s",

            secid,

        )





        self.load_indices()






        result = self._items.get(

            secid,

            [],

        )






        logger.debug(

            "INDEX AFTER LOAD SECID=%s COUNT=%s",

            secid,

            len(result),

        )





        return result










    def get(
        self,
        secid: str,
    ) -> SecurityModel:



        secid = secid.upper()





        variants = self.get_all(

            secid

        )






        if not variants:


            logger.error(

                "INDEX NOT FOUND SECID=%s",

                secid,

            )


            raise ValueError(

                f"Индекс '{secid}' не найден"

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

            "PRIMARY INDEX SELECTED SECID=%s BOARD=%s",

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

            "CHECK INDEX EXISTS SECID=%s RESULT=%s",

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

            "INDEX CATALOG COUNT=%s",

            total,

        )



        return total