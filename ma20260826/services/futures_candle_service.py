from __future__ import annotations


from typing import Any


from client.moex_client import MoexClient


from models.candle_model import CandleModel
from models.futures_model import FuturesModel


from services.futures_service import FuturesService


from utils.datetime_utils import parse_moscow_datetime
from utils.logger import get_logger



logger = get_logger(__name__)





BOARD_PRIORITY = {

    "RFUD": 100,

}








class FuturesCandleService:
    """
    Сервис получения свечей фьючерсов MOEX.


    Источник:

        FuturesService


    Рынок:

        futures / forts


    Поддерживает:

        interval=24
            дневные свечи


        interval=1
            минутные свечи


    Возможности:

    - поиск конкретного контракта
    - поиск по asset_code
    - выбор торговой доски
    - пагинация ISS
    - московское время

    """



    PAGE_SIZE = 500



    ENGINE = "futures"


    MARKET = "forts"







    def __init__(
        self,
        client: MoexClient,
        futures_service: FuturesService,
    ) -> None:


        self.client = client


        self.futures_service = futures_service



        logger.debug(

            "FuturesCandleService initialized"

        )









    # --------------------------------------------------
    # PARSER
    # --------------------------------------------------


    @staticmethod
    def _parse_table(
        response: dict[str, Any],
        table_name: str,
    ) -> list[dict[str, Any]]:


        table = response.get(

            table_name

        )


        if not table:

            return []



        columns = table.get(

            "columns",

            []

        )


        rows = table.get(

            "data",

            []

        )



        return [

            dict(

                zip(

                    columns,

                    row,

                )

            )

            for row in rows

        ]









    @staticmethod
    def _safe_float(
        value: Any,
    ) -> float:


        try:

            return float(

                value or 0

            )


        except Exception:

            return 0.0









    @staticmethod
    def _safe_int(
        value: Any,
    ) -> int:


        try:

            return int(

                value or 0

            )


        except Exception:

            return 0









    @staticmethod
    def _parse_datetime(
        value: Any,
    ):


        if not value:

            return None



        return parse_moscow_datetime(

            value

        )









    # --------------------------------------------------
    # FIND FUTURE
    # --------------------------------------------------


    def _find_future(
        self,
        secid: str,
    ) -> FuturesModel:


        """
        Поиск конкретного контракта.


        Приоритет:

        1. SECID контракта

            BRU6


        2. asset_code

            BR

        """



        logger.debug(

            "FIND FUTURES CONTRACT SECID=%s",

            secid,

        )



        # ----------------------------------------------
        # 1. Прямой поиск контракта
        # ----------------------------------------------

        try:


            future = self.futures_service.get(

                secid

            )


            if future:


                logger.info(

                    "FUTURES CONTRACT FOUND SECID=%s",

                    future.secid,

                )


                return future



        except Exception as error:


            logger.debug(

                "DIRECT FUTURES SEARCH FAILED SECID=%s ERROR=%s",

                secid,

                error,

            )




        # ----------------------------------------------
        # 2. Поиск группы контрактов
        # ----------------------------------------------


        futures = self.futures_service.get_all(

            secid

        )



        if not futures:


            raise ValueError(

                f"Фьючерс '{secid}' не найден"

            )



        futures = sorted(

            futures,

            key=lambda x:

            BOARD_PRIORITY.get(

                x.board,

                0,

            ),

            reverse=True,

        )



        selected = futures[0]



        logger.info(

            "FUTURES FROM GROUP SELECTED SECID=%s",

            selected.secid,

        )



        return selected









    # --------------------------------------------------
    # MOEX REQUEST
    # --------------------------------------------------


    def _request_candles(
        self,
        future: FuturesModel,
        date_from: str,
        date_till: str,
        interval: int,
    ) -> list[dict[str, Any]]:



        logger.debug(

            """
TRY FUTURES CANDLES

SECID=%s
BOARD=%s
FROM=%s
TILL=%s
INTERVAL=%s

""",

            future.secid,

            future.board,

            date_from,

            date_till,

            interval,

        )



        result = []


        start = 0


        page = 1




        while True:


            response = self.client.get_candles(

                engine=self.ENGINE,

                market=self.MARKET,

                security=future.secid,

                date_from=date_from,

                date_till=date_till,

                interval=interval,

                start=start,

            )



            candles = self._parse_table(

                response,

                "candles",

            )



            if not candles:

                break



            result.extend(

                candles

            )



            logger.debug(

                "FUTURES PAGE=%s COUNT=%s",

                page,

                len(candles),

            )



            if len(candles) < self.PAGE_SIZE:

                break



            start += self.PAGE_SIZE


            page += 1




        return result










    # --------------------------------------------------
    # PUBLIC API
    # --------------------------------------------------


    def get(
        self,
        secid: str,
        date_from: str,
        date_till: str,
        interval: int = 24,
    ) -> list[CandleModel]:


        logger.debug(

            "GET FUTURES CANDLES SECID=%s",

            secid,

        )



        future = self._find_future(

            secid

        )



        candles_data = self._request_candles(

            future,

            date_from,

            date_till,

            interval,

        )



        if not candles_data:


            logger.warning(

                "NO FUTURES CANDLES SECID=%s",

                secid,

            )


            return []




        result = []


        seen = set()



        for item in candles_data:


            begin = self._parse_datetime(

                item.get(

                    "begin"

                )

            )



            if begin is None:

                continue



            if begin in seen:

                continue



            seen.add(

                begin

            )




            result.append(

                CandleModel(

                    secid=future.secid,


                    ticker=future.secid,


                    name=future.shortname,



                    engine=self.ENGINE,


                    market=self.MARKET,


                    board=future.board,



                    begin=begin,



                    end=self._parse_datetime(

                        item.get(

                            "end"

                        )

                    ),



                    open=self._safe_float(

                        item.get(

                            "open"

                        )

                    ),



                    high=self._safe_float(

                        item.get(

                            "high"

                        )

                    ),



                    low=self._safe_float(

                        item.get(

                            "low"

                        )

                    ),



                    close=self._safe_float(

                        item.get(

                            "close"

                        )

                    ),



                    volume=self._safe_int(

                        item.get(

                            "volume"

                        )

                    ),



                    value=self._safe_float(

                        item.get(

                            "value"

                        )

                    ),

                )

            )





        result.sort(

            key=lambda x:

            x.begin

        )





        logger.info(

            """
FUTURES CANDLES READY

SECID=%s
BOARD=%s
COUNT=%s

""",

            future.secid,

            future.board,

            len(result),

        )




        return result