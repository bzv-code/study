from __future__ import annotations


from typing import Any


from client.moex_client import MoexClient

from models.candle_model import CandleModel
from models.stock_model import StockModel

from services.stock_service import StockService

from utils.datetime_utils import parse_moscow_datetime
from utils.logger import get_logger



logger = get_logger(__name__)





BOARD_PRIORITY = {

    # Основная торговая доска акций
    "TQBR": 100,


    # Техническая доска
    "SMAL": 90,


    # SPEQ
    "SPEQ": 80,


    # Технические
    "TQTF": 70,

}






class StockCandleService:
    """
    Сервис получения свечей акций MOEX.

    Отдельно от общего CandleService.

    Источник:

        StockService


    Поддерживает:

        interval=24
            дневные свечи

        interval=1
            минутные свечи


    Возможности:

    - выбор торговой доски
    - загрузка страниц ISS
    - защита дублей
    - московское время
    """



    PAGE_SIZE = 500





    def __init__(
        self,
        client: MoexClient,
        stock_service: StockService,
    ) -> None:


        self.client = client

        self.stock_service = stock_service


        logger.debug(
            "StockCandleService initialized"
        )






    # --------------------------------------------------
    # MOEX TABLE PARSER
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
    # LOAD MOEX CANDLES
    # --------------------------------------------------


    def _request_candles(
        self,
        stock: StockModel,
        date_from: str,
        date_till: str,
        interval: int,
    ) -> list[dict[str, Any]]:


        logger.debug(

            """
TRY STOCK CANDLES

SECID: %s
BOARD: %s
INTERVAL: %s
FROM: %s
TILL: %s
""",

            stock.secid,
            stock.board,
            interval,
            date_from,
            date_till,

        )



        result = []


        start = 0


        page = 1



        while True:


            response = self.client.get_candles(

                engine=stock.engine,

                market=stock.market,

                security=stock.secid,

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

                "PAGE=%s RECEIVED=%s",

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

            "GET STOCK CANDLES SECID=%s",

            secid,

        )



        variants = self.stock_service.get_all(

            secid

        )



        if not variants:


            self.stock_service.exists(

                secid

            )


            variants = self.stock_service.get_all(

                secid

            )



        if not variants:


            raise ValueError(

                f"Акция '{secid}' не найдена"

            )



        variants = sorted(

            variants,

            key=lambda x:

            BOARD_PRIORITY.get(

                x.board,

                0,

            ),

            reverse=True,

        )



        candles_data = []


        selected: StockModel | None = None



        for stock in variants:


            candles_data = self._request_candles(

                stock,

                date_from,

                date_till,

                interval,

            )


            if candles_data:


                selected = stock

                break





        if not candles_data:


            logger.warning(

                "NO STOCK CANDLES SECID=%s",

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

                    secid=selected.secid,

                    ticker=selected.secid,

                    name=selected.shortname,


                    engine=selected.engine,

                    market=selected.market,

                    board=selected.board,


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

            "STOCK CANDLES READY SECID=%s COUNT=%s BOARD=%s",

            secid,

            len(result),

            selected.board,

        )



        return result