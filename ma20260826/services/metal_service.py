from __future__ import annotations


from models.metal_model import MetalModel

from services.candle_service import CandleService

from utils.datetime_utils import parse_moscow_datetime

from utils.logger import get_logger



logger = get_logger(__name__)





class MetalService:
    """
    Сервис работы с драгоценными металлами MOEX.

    Поддерживает таймфреймы:

        1   - минута
        10  - 10 минут
        60  - час
        24  - день


    Все даты приводятся к:

        Europe/Moscow
    """





    METALS: dict[str, str] = {


        "GLDRUB_TOM": "Золото",


        "SLVRUB_TOM": "Серебро",


        "PLTRUB_TOM": "Платина",


        "PLDRUB_TOM": "Палладий",


    }





    def __init__(
        self,
        candle_service: CandleService,
    ) -> None:


        self.candle_service = candle_service



        logger.debug(
            "MetalService initialized"
        )






    def get_prices(
        self,
        secid: str,
        date_from: str,
        date_till: str,
        interval: int = 24,
    ) -> list[MetalModel]:
        """
        Получить свечи одного металла.
        """



        logger.info(

            "LOAD METAL PRICES SECID=%s FROM=%s TO=%s INTERVAL=%s",

            secid,

            date_from,

            date_till,

            interval,

        )





        candles = self.candle_service.get(


            secid=secid,


            date_from=date_from,


            date_till=date_till,


            interval=interval,


        )





        logger.debug(

            "CANDLES RECEIVED SECID=%s COUNT=%s",

            secid,

            len(candles),

        )





        result: list[MetalModel] = []





        for candle in candles:



            result.append(



                MetalModel(



                    ticker=candle.secid,



                    name=self.METALS.get(



                        candle.secid,



                        candle.secid,



                    ),



                    engine=candle.engine,



                    market=candle.market,



                    board=candle.board,





                    # МСК время

                    date=parse_moscow_datetime(



                        candle.begin



                    ),






                    open=candle.open,



                    high=candle.high,



                    low=candle.low,



                    close=candle.close,





                    volume=candle.volume,



                    value=candle.value,



                )



            )







        logger.info(

            "METAL READY SECID=%s ROWS=%s",

            secid,

            len(result),

        )




        if not result:


            logger.warning(

                "NO METAL DATA SECID=%s",

                secid,

            )



        return result







    def get_all_prices(
        self,
        date_from: str,
        date_till: str,
        interval: int = 24,
    ) -> list[MetalModel]:
        """
        Получить все металлы.
        """



        logger.info(

            "LOAD ALL METALS FROM=%s TO=%s INTERVAL=%s",

            date_from,

            date_till,

            interval,

        )





        result: list[MetalModel] = []





        for secid in self.METALS:



            logger.debug(

                "PROCESS METAL SECID=%s",

                secid,

            )





            prices = self.get_prices(



                secid=secid,



                date_from=date_from,



                date_till=date_till,



                interval=interval,



            )





            result.extend(

                prices

            )







        logger.info(

            "ALL METALS READY TOTAL_ROWS=%s",

            len(result),

        )





        return result