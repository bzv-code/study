from __future__ import annotations


from collections import defaultdict
from typing import Final


import httpx


from client.moex_client import MoexClient

from models.stock_model import StockModel

from services.sector_service import SectorService

from utils.iss_parser import IssParser
from utils.logger import get_logger



logger = get_logger(__name__)





BOARD_PRIORITY: Final[dict[str, int]] = {


    # Основная торговая доска акций
    "TQBR": 100,


    # ETF
    "TQTF": 90,


    # Дополнительные варианты
    "SMAL": 50,

    "SPEQ": 40,

}






class StockCatalog:
    """
    Каталог акций MOEX.

    Загружает:

        stock / shares


    Возвращает:

        StockModel


    Дополнительные данные:

        isin
        sector


    sector добавляется через SectorService.
    """



    SEARCH_MARKETS = [

        (
            "stock",
            "shares",
        ),

    ]


    LOAD_LIMIT = 5000





    def __init__(
        self,
        client: MoexClient,
        sector_service: SectorService | None = None,
    ) -> None:


        self.client = client


        self.sector_service = sector_service



        self._items: dict[
            str,
            list[StockModel],
        ] = defaultdict(list)



        self._loaded_markets: set[
            tuple[str, str]
        ] = set()



        logger.debug(
            "StockCatalog initialized"
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
            "LOAD STOCK MARKET %s/%s",
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

                "LOAD STOCK MARKET ERROR %s/%s ERROR=%s",

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

            "STOCK MARKET LOADED %s/%s COUNT=%s",

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

            "STOCK CACHE UPDATED TOTAL=%s",

            self.count(),

        )









    # ==================================================
    # Добавление акции
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


            logger.warning(
                "SKIP STOCK WITHOUT SECID"
            )


            return






        isin = str(

            row.get(

                "ISIN",

                "",

            )

            or ""

        )






        stock = StockModel(



            secid=secid,


            isin=isin,



            shortname=str(

                row.get(
                    "SHORTNAME",
                    ""
                )

                or ""

            ),



            name=str(

                row.get(
                    "SECNAME",
                    ""
                )

                or ""

            ),



            secname=str(

                row.get(
                    "SECNAME",
                    ""
                )

                or ""

            ),



            engine=engine,


            market=market,



            board=str(

                row.get(
                    "BOARDID",
                    ""
                )

                or ""

            ),



            board_title=str(

                row.get(
                    "BOARDNAME",
                    ""
                )

                or ""

            ),




            currency=str(

                row.get(
                    "FACEUNIT",
                    ""
                )

                or ""

            ),




            decimals=self._safe_int(

                row.get(
                    "DECIMALS"
                )

            ),




            lotsize=self._safe_int(

                row.get(
                    "LOTSIZE"
                )

            ),



            trading_status=str(

                row.get(
                    "STATUS",
                    ""
                )

                or ""

            ),



        )



        if self.sector_service:


            stock = self.sector_service.enrich(

                stock

            )





        exists = any(

            x.engine == stock.engine

            and x.market == stock.market

            and x.board == stock.board


            for x in self._items[secid]

        )





        if exists:

            return





        self._items[secid].append(

            stock

        )





        logger.debug(

            "ADD STOCK SECID=%s BOARD=%s ISIN=%s SECTOR=%s",

            stock.secid,

            stock.board,

            stock.isin,

            stock.sector,

        )









    # ==================================================
    # Utils
    # ==================================================


    @staticmethod
    def _safe_int(
        value,
    ) -> int:


        try:

            return int(
                value or 0
            )

        except Exception:

            return 0







    # ==================================================
    # Загрузка акций
    # ==================================================


    def load_stocks(
        self,
    ) -> None:


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
    ) -> list[StockModel]:


        if not secid:

            return []



        secid = secid.upper()



        result = self._items.get(

            secid,

            [],

        )



        if not result:


            self.load_stocks()


            result = self._items.get(

                secid,

                [],

            )





        return sorted(

            result,

            key=lambda x:

            BOARD_PRIORITY.get(

                x.board,

                0,

            ),

            reverse=True,

        )









    def get(
        self,
        secid: str,
    ) -> StockModel:



        variants = self.get_all(

            secid

        )



        if not variants:


            raise ValueError(

                f"Акция '{secid}' не найдена"

            )





        selected = variants[0]




        logger.info(

            "PRIMARY STOCK SELECTED SECID=%s BOARD=%s",

            selected.secid,

            selected.board,

        )




        return selected









    def get_all_items(
        self,
    ) -> list[StockModel]:


        self.load_stocks()


        result = []


        for items in self._items.values():

            result.extend(items)



        return result










    def exists(
        self,
        secid: str,
    ) -> bool:


        return bool(

            self.get_all(secid)

        )









    def search(
        self,
        text: str,
    ) -> list[StockModel]:


        if not text:

            return []



        self.load_stocks()



        text = text.upper()



        result = []



        for items in self._items.values():


            for item in items:


                if (

                    text in item.secid.upper()

                    or text in item.shortname.upper()

                    or text in item.isin.upper()

                ):


                    result.append(item)



        return result










    def count(
        self,
    ) -> int:


        return sum(

            len(items)

            for items in self._items.values()

        )