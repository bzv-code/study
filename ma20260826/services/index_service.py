from __future__ import annotations


from models.index_model import IndexModel


from services.candle_service import CandleService


from catalog.index_catalog import IndexCatalog


from utils.datetime_utils import parse_moscow_datetime

from utils.logger import get_logger




logger = get_logger(__name__)







class IndexService:
    """
    Сервис работы с индексами MOEX.


    Таймфреймы MOEX:

        1   - минута
        10  - 10 минут
        60  - час
        24  - день
        7   - неделя
        31  - месяц


    Все даты:

        Europe/Moscow
    """



    INDEXES: list[str] = [


        "IMOEX",

        "RTSI",


        "MOEXOG",

        "MOEXEU",

        "MOEXFN",

        "MOEXMM",

        "MOEXTN",

        "MOEXCH",

        "MOEXCN",

        "MOEXTL",

        "MOEXRE",

        "MOEXIT",


        "RGBITR",

        "RUSFAR",

        "RGBI",


        "MOEX10",


        "RUCBTRNS",

        "RUSFARCNY",


        "MOEXINN",


        "WHFOB",


        "MCFTR",


        "MOEXBTC",


        "RBCRED",

        "RBCSPARK",

        "RBCWHITE",


    ]









    def __init__(
        self,
        candle_service: CandleService,
        index_catalog: IndexCatalog,
    ) -> None:



        self.candle_service = candle_service

        self.index_catalog = index_catalog



        logger.debug(

            "IndexService initialized"

        )









    def get_prices(
        self,
        secid: str,
        date_from: str,
        date_till: str,
        interval: int = 24,
    ) -> list[IndexModel]:
        """
        Получить свечи одного индекса.
        """



        secid = secid.upper()





        logger.info(

            "LOAD INDEX PRICES SECID=%s FROM=%s TO=%s INTERVAL=%s",

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







        name = secid





        try:


            security = self.index_catalog.get(

                secid

            )


            name = (

                security.shortname

                or secid

            )



            logger.debug(

                "INDEX INFO SECID=%s NAME=%s BOARD=%s",

                secid,

                name,

                security.board,

            )




        except ValueError:


            logger.warning(

                "INDEX NOT FOUND IN CATALOG SECID=%s",

                secid,

            )



        except Exception as error:


            logger.exception(

                "INDEX CATALOG ERROR SECID=%s ERROR=%s",

                secid,

                error,

            )









        result: list[IndexModel] = []







        for candle in candles:



            result.append(



                IndexModel(


                    ticker=candle.secid,


                    name=name,


                    engine=candle.engine,


                    market=candle.market,


                    board=candle.board,



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

            "INDEX READY SECID=%s ROWS=%s",

            secid,

            len(result),

        )








        if not result:


            logger.warning(

                "NO INDEX DATA SECID=%s",

                secid,

            )





        return result














    def get_all_prices(
        self,
        date_from: str,
        date_till: str,
        interval: int = 24,
    ) -> list[IndexModel]:
        """
        Получить свечи всех индексов MOEX.
        """



        logger.info(

            "LOAD ALL INDICES FROM=%s TO=%s INTERVAL=%s",

            date_from,

            date_till,

            interval,

        )





        result: list[IndexModel] = []







        for secid in self.INDEXES:



            logger.debug(

                "PROCESS INDEX SECID=%s",

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

            "ALL INDICES READY TOTAL_ROWS=%s",

            len(result),

        )






        return result