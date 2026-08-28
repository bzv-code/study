from __future__ import annotations


from collections import defaultdict
from datetime import date
from typing import Final


import httpx


from client.moex_client import MoexClient


from models.futures_model import FuturesModel


from utils.iss_parser import IssParser

from utils.logger import get_logger





logger = get_logger(__name__)





FUTURES_PRIORITY: Final[dict[str, int]] = {

    # основной рынок фьючерсов
    "RFUD": 100,

}









class FuturesCatalog:
    """
    Каталог фьючерсов MOEX.


    Источник:

        MOEX ISS

        /iss/engines/futures/markets/forts/securities.json


    Возвращает:

        FuturesModel


    Используется:

        FuturesService

        Futures analytics

        ClickHouse writer

    """



    ENGINE = "futures"


    MARKET = "forts"



    LOAD_LIMIT = 5000







    def __init__(
        self,
        client: MoexClient,
    ) -> None:


        self.client = client



        self._items: dict[
            str,
            list[FuturesModel],
        ] = defaultdict(list)



        self._loaded = False



        logger.debug(
            "FuturesCatalog initialized"
        )









    # ==================================================
    # Load
    # ==================================================


    def load_futures(
        self,
    ) -> None:
        """
        Загрузка списка фьючерсов MOEX.
        """



        if self._loaded:


            logger.debug(
                "FUTURES ALREADY LOADED"
            )


            return





        logger.info(
            "LOAD FUTURES MARKET"
        )



        try:


            response = self.client.get(

                "/engines/futures/markets/forts/securities.json"

            )



        except httpx.HTTPError as error:


            logger.exception(

                "LOAD FUTURES ERROR=%s",

                error,

            )


            return





        rows = IssParser.table(

            response,

            "securities",

        )




        logger.info(

            "FUTURES LOADED COUNT=%s",

            len(rows),

        )




        for row in rows:


            self._add(

                row

            )




        self._loaded = True




        logger.debug(

            "FUTURES CACHE SIZE=%s",

            self.count(),

        )









    # ==================================================
    # Add
    # ==================================================


    def _add(
        self,
        row: dict,
    ) -> None:
        """
        Добавление фьючерса в каталог.
        """



        secid = str(

            row.get(

                "SECID",

                "",

            )

        ).upper()





        if not secid:


            logger.warning(
                "SKIP FUTURES WITHOUT SECID"
            )


            return





        future = FuturesModel(



            secid=secid,



            board=str(

                row.get(

                    "BOARDID",

                    ""

                )

                or ""

            ),





            shortname=str(

                row.get(

                    "SHORTNAME",

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






            latname=str(

                row.get(

                    "LATNAME",

                    ""

                )

                or ""

            ),





            asset_code=str(

                row.get(

                    "ASSETCODE",

                    ""

                )

                or ""

            ),





            sectype=str(

                row.get(

                    "SECTYPE",

                    ""

                )

                or ""

            ),






            prev_settle_price=self._safe_float(

                row.get(

                    "PREVSETTLEPRICE"

                )

            ),



            last_settle_price=self._safe_float(

                row.get(

                    "LASTSETTLEPRICE"

                )

            ),



            settle_price_clr=self._safe_float(

                row.get(

                    "SETTLEPRICE_CLR"

                )

            ),



            prev_price=self._safe_float(

                row.get(

                    "PREVPRICE"

                )

            ),





            decimals=self._safe_int(

                row.get(

                    "DECIMALS"

                )

            ),




            min_step=self._safe_float(

                row.get(

                    "MINSTEP"

                )

            ),




            step_price=self._safe_float(

                row.get(

                    "STEPPRICE"

                )

            ),





            lot_volume=self._safe_int(

                row.get(

                    "LOTVOLUME"

                )

            ),





            initial_margin=self._safe_float(

                row.get(

                    "INITIALMARGIN"

                )

            ),




            high_limit=self._safe_float(

                row.get(

                    "HIGHLIMIT"

                )

            ),




            low_limit=self._safe_float(

                row.get(

                    "LOWLIMIT"

                )

            ),




            prev_open_position=self._safe_int(

                row.get(

                    "PREVOPENPOSITION"

                )

            ),




            last_trade_date=self._parse_date(

                row.get(

                    "LASTTRADEDATE"

                )

            ),





            last_delivery_date=self._parse_date(

                row.get(

                    "LASTDELDATE"

                )

            ),





            buy_sell_fee=self._safe_float(

                row.get(

                    "BUYSELLFEE"

                )

            ),





            scalper_fee=self._safe_float(

                row.get(

                    "SCALPERFEE"

                )

            ),





            negotiated_fee=self._safe_float(

                row.get(

                    "NEGOTIATEDFEE"

                )

            ),





            exercise_fee=self._safe_float(

                row.get(

                    "EXERCISEFEE"

                )

            ),





        )





        exists = any(

            x.board == future.board

            for x in self._items[secid]

        )





        if exists:

            return





        self._items[secid].append(

            future

        )





        logger.debug(

            "ADD FUTURES SECID=%s BOARD=%s ASSET=%s",

            future.secid,

            future.board,

            future.asset_code,

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







    @staticmethod
    def _safe_float(
        value,
    ) -> float:


        try:

            return float(

                value or 0

            )


        except Exception:

            return 0.0







    @staticmethod
    def _parse_date(
        value,
    ) -> date | None:


        if not value:

            return None



        try:

            return date.fromisoformat(

                str(value)

            )


        except Exception:

            return None







    # ==================================================
    # API
    # ==================================================


    def get_all(
        self,
        secid: str,
    ) -> list[FuturesModel]:


        if not secid:

            return []



        secid = secid.upper()



        result = self._items.get(

            secid,

            [],

        )



        if not result:


            self.load_futures()



            result = self._items.get(

                secid,

                [],

            )




        return sorted(

            result,

            key=lambda x:

            x.last_delivery_date

            or date.max

        )









    def get(
        self,
        secid: str,
    ) -> FuturesModel:


        items = self.get_all(

            secid

        )



        if not items:


            raise ValueError(

                f"Фьючерс '{secid}' не найден"

            )



        selected = items[0]



        logger.info(

            "PRIMARY FUTURES SELECTED SECID=%s EXP=%s",

            selected.secid,

            selected.last_delivery_date,

        )



        return selected









    def get_all_items(
        self,
    ) -> list[FuturesModel]:


        self.load_futures()



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
    ) -> list[FuturesModel]:


        if not text:

            return []



        self.load_futures()



        text = text.upper()



        result = []



        for items in self._items.values():


            for item in items:



                if (

                    text in item.secid.upper()

                    or text in item.asset_code.upper()

                    or text in item.shortname.upper()

                    or text in item.secname.upper()

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