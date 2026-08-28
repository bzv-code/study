from __future__ import annotations


from client.moex_client import MoexClient

from catalog.instrument_catalog import InstrumentCatalog

from services.security_service import SecurityService
from services.candle_service import CandleService

from utils.rate_limiter import RateLimiter
from utils.logger import get_logger


from database.client_clickhouse import ClickHouseClient

from database.currency.currency_clickhouse import CurrencyClickHouse

from database.currency.writer_currency_d_clickhouse import (
    CurrencyDWriterClickHouse,
)



logger = get_logger(__name__)





DATE_FROM = "2000-01-01"

DATE_TO = "2026-07-31"





SECIDS = [

    "CNYRUB_TOM",

    "TRYRUB_TOM",

    "KZTRUB_TOM",

    "BYNRUB_TOM",

    "AMDRUB_TOM",

]





# MOEX
# дневные свечи

INTERVAL = 24






limiter = RateLimiter(

    max_requests=3

)





all_currencies = []







logger.info(

    "START RUN CURRENCY D"

)



logger.info(

    "DATE FROM=%s DATE TO=%s INTERVAL=%s",

    DATE_FROM,

    DATE_TO,

    INTERVAL,

)



logger.info(

    "SECIDS=%s",

    SECIDS,

)










# ------------------------------------------------------
# Загрузка данных MOEX
# ------------------------------------------------------

with MoexClient() as client:



    logger.info(

        "MOEX CLIENT CREATED"

    )





    catalog = InstrumentCatalog(

        client

    )





    security_service = SecurityService(

        catalog

    )





    candle_service = CandleService(

        client,

        security_service,

    )





    logger.info(

        "SERVICES INITIALIZED"

    )







    for secid in SECIDS:



        logger.info(

            "LOAD MOEX CURRENCY SECID=%s",

            secid,

        )





        limiter.wait()






        candles = candle_service.get(


            secid=secid,


            date_from=DATE_FROM,


            date_till=DATE_TO,


            interval=INTERVAL,


        )





        logger.info(

            "RECEIVED SECID=%s ROWS=%s",

            secid,

            len(candles),

        )





        all_currencies.extend(

            candles

        )









# ------------------------------------------------------
# Сортировка
# ------------------------------------------------------

all_currencies.sort(

    key=lambda x: (

        x.ticker,

        x.begin,

    )

)





logger.info(

    "TOTAL DATA ROWS=%s",

    len(all_currencies),

)










# ------------------------------------------------------
# Загрузка в ClickHouse
# ------------------------------------------------------

if all_currencies:



    logger.info(

        "START CLICKHOUSE INSERT"

    )





    with ClickHouseClient() as client:



        currency_clickhouse = CurrencyClickHouse(


            client,


            table_name="moex_api.moex_currency_d"


        )





        writer = CurrencyDWriterClickHouse(


            currency_clickhouse


        )





        writer.write(

            all_currencies

        )





    logger.info(

        "CLICKHOUSE INSERT FINISHED"

    )







else:



    logger.warning(

        "NO DATA RECEIVED"

    )









logger.info(

    "RUN COMPLETE CURRENCY D"

)