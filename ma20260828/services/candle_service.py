from __future__ import annotations


from typing import Any


from client.moex_client import MoexClient

from models.candle_model import CandleModel
from models.security_model import SecurityModel

from services.security_service import SecurityService

from utils.datetime_utils import parse_moscow_datetime
from utils.logger import get_logger



logger = get_logger(__name__)




BOARD_PRIORITY = {

    "CETS": 100,

    "LICU": 90,

    "CNGD": 80,

    "TQBR": 70,

    "TQOB": 60,

    "RFUD": 50,

}




class CandleService:
    """
    Универсальный сервис получения свечей MOEX.

    Поддерживает:

        interval=24
            дневные свечи

        interval=1
            минутные свечи


    Возможности:

    - несколько BOARD
    - выбор приоритетной площадки
    - постраничная загрузка ISS
    - защита от дублей
    - московское время
    """



    PAGE_SIZE = 500



    def __init__(
        self,
        client: MoexClient,
        security_service: SecurityService,
    ) -> None:

        self.client = client

        self.security_service = security_service


        logger.debug(
            "CandleService initialized"
        )



    @staticmethod
    def _parse_table(
        response: dict[str, Any],
        table_name: str,
    ) -> list[dict[str, Any]]:


        table = response.get(
            table_name
        )


        if not table:

            logger.debug(
                "MOEX response has no table: %s",
                table_name,
            )

            return []



        columns = table.get(
            "columns",
            []
        )


        rows = table.get(
            "data",
            []
        )


        result = [

            dict(
                zip(
                    columns,
                    row,
                )
            )

            for row in rows

        ]


        logger.debug(
            "PARSE TABLE=%s ROWS=%s",
            table_name,
            len(result),
        )


        return result




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





    def _request_candles(
        self,
        security: SecurityModel,
        date_from: str,
        date_till: str,
        interval: int,
    ) -> list[dict[str, Any]]:


        logger.debug(
            """
TRY CANDLES

SECID: %s
ENGINE: %s
MARKET: %s
BOARD: %s
INTERVAL: %s
DATE FROM: %s
DATE TILL: %s
""",
            security.secid,
            security.engine,
            security.market,
            security.board,
            interval,
            date_from,
            date_till,
        )



        all_candles: list[dict[str, Any]] = []


        start = 0

        page = 1



        while True:


            logger.debug(
                "LOAD PAGE=%s START=%s",
                page,
                start,
            )



            response = self.client.get_candles(

                engine=security.engine,

                market=security.market,

                security=security.secid,

                date_from=date_from,

                date_till=date_till,

                interval=interval,

                start=start,

            )



            candles = self._parse_table(

                response,

                "candles",

            )



            count = len(candles)



            logger.debug(
                "PAGE RECEIVED PAGE=%s COUNT=%s",
                page,
                count,
            )



            if not candles:

                break



            all_candles.extend(
                candles
            )



            if count < self.PAGE_SIZE:

                break



            start += self.PAGE_SIZE

            page += 1




        logger.info(
            "TOTAL CANDLES RECEIVED SECID=%s COUNT=%s",
            security.secid,
            len(all_candles),
        )


        return all_candles





    def get(
        self,
        secid: str,
        date_from: str,
        date_till: str,
        interval: int = 24,
    ) -> list[CandleModel]:
        """
        Получение исторических свечей.
        """



        logger.debug(
            "GET CANDLES SECID=%s INTERVAL=%s",
            secid,
            interval,
        )



        variants = self.security_service.get_all(
            secid
        )



        logger.debug(
            "SECURITY VARIANTS FOUND=%s",
            len(variants),
        )



        if not variants:


            logger.debug(
                "SECURITY NOT IN CACHE CHECK EXISTS SECID=%s",
                secid,
            )


            self.security_service.exists(
                secid
            )


            variants = self.security_service.get_all(
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



        variants = sorted(

            variants,

            key=lambda x:

            BOARD_PRIORITY.get(
                x.board,
                0,
            ),

            reverse=True,

        )



        logger.debug(
            "SORTED BOARDS=%s",
            [
                x.board
                for x in variants
            ],
        )



        candles_data: list[dict[str, Any]] = []

        selected_security: SecurityModel | None = None



        for security in variants:


            candles_data = self._request_candles(

                security,

                date_from,

                date_till,

                interval,

            )


            if candles_data:

                selected_security = security

                break



        if not candles_data:

            logger.warning(
                "NO CANDLES FOUND SECID=%s",
                secid,
            )

            return []



        logger.info(
            "FOUND BOARD=%s SECID=%s",
            selected_security.board,
            secid,
        )



        result: list[CandleModel] = []

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

                    secid=selected_security.secid,

                    ticker=selected_security.secid,

                    name=getattr(
                        selected_security,
                        "shortname",
                        ""
                    ),

                    engine=selected_security.engine,

                    market=selected_security.market,

                    board=selected_security.board,


                    begin=begin,


                    end=self._parse_datetime(

                        item.get(
                            "end"
                        )

                    ),


                    open=self._safe_float(
                        item.get("open")
                    ),

                    high=self._safe_float(
                        item.get("high")
                    ),

                    low=self._safe_float(
                        item.get("low")
                    ),

                    close=self._safe_float(
                        item.get("close")
                    ),


                    volume=self._safe_int(
                        item.get("volume")
                    ),


                    value=self._safe_float(
                        item.get("value")
                    ),

                )

            )



        result.sort(
            key=lambda x: x.begin
        )



        logger.info(
            "RESULT CANDLES SECID=%s COUNT=%s",
            secid,
            len(result),
        )



        return result