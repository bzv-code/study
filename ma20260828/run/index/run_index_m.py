from __future__ import annotations


from client.moex_client import MoexClient


from catalog.index_catalog import IndexCatalog


from services.security_service import SecurityService
from services.candle_service import CandleService
from services.index_service import IndexService


from utils.rate_limiter import RateLimiter
from utils.logger import get_logger


from database.client_clickhouse import ClickHouseClient


from database.index.index_clickhouse import IndexClickHouse


from database.index.writer_index_m_clickhouse import (
    IndexMWriterClickHouse,
)





logger = get_logger(__name__)





DATE_FROM = "2000-01-01"


DATE_TO = "2026-07-31"







SECIDS = [

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

    "WHFOB",

    "MCFTR",

    "MOEXBTC",

    "RBCRED",

    "RBCSPARK",

    "RBCWHITE",

]






# ------------------------------------------------------
# MOEX
# месячные свечи
# ------------------------------------------------------

INTERVAL = 31






limiter = RateLimiter(

    max_requests=3

)





all_indices = []







logger.info(

    "START RUN INDEX M"

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




    index_catalog = IndexCatalog(

        client

    )




    security_service = SecurityService(

        index_catalog

    )




    candle_service = CandleService(

        client,

        security_service,

    )




    index_service = IndexService(

        candle_service,

        index_catalog,

    )




    logger.info(

        "SERVICES INITIALIZED"

    )





    for secid in SECIDS:



        logger.info(

            "LOAD MOEX INDEX SECID=%s",

            secid,

        )




        limiter.wait()





        try:



            prices = index_service.get_prices(

                secid=secid,

                date_from=DATE_FROM,

                date_till=DATE_TO,

                interval=INTERVAL,

            )





        except Exception as error:



            logger.exception(

                "INDEX LOAD ERROR SECID=%s ERROR=%s",

                secid,

                error,

            )



            continue






        logger.info(

            "RECEIVED SECID=%s ROWS=%s",

            secid,

            len(prices),

        )





        all_indices.extend(

            prices

        )









# ------------------------------------------------------
# Сортировка
# ------------------------------------------------------

all_indices.sort(

    key=lambda x: (

        x.ticker,

        x.date,

    )

)





logger.info(

    "TOTAL DATA ROWS=%s",

    len(all_indices),

)









# ------------------------------------------------------
# Загрузка в ClickHouse
# ------------------------------------------------------

if all_indices:



    logger.info(

        "START CLICKHOUSE INSERT"

    )





    with ClickHouseClient() as client:




        index_clickhouse = IndexClickHouse(

            client,

            table_name="moex_api.moex_index_m",

        )





        writer = IndexMWriterClickHouse(

            index_clickhouse,

        )





        writer.write(

            all_indices,

        )







    logger.info(

        "CLICKHOUSE INSERT FINISHED"

    )





else:



    logger.warning(

        "NO DATA RECEIVED"

    )








logger.info(

    "RUN COMPLETE INDEX M"

)