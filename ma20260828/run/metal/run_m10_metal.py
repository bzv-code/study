from __future__ import annotations


from client.moex_client import MoexClient

from catalog.instrument_catalog import InstrumentCatalog

from services.security_service import SecurityService
from services.candle_service import CandleService
from services.metal_service import MetalService

from utils.rate_limiter import RateLimiter
from utils.logger import get_logger


from database.client_clickhouse import ClickHouseClient
from database.metal.metal_clickhouse import MetalClickHouse

from database.metal.writer_metal_m10_clickhouse import (
    MetalM10WriterClickHouse,
)



logger = get_logger(__name__)




DATE_FROM = "2000-01-01"

DATE_TO = "2015-12-31"



SECIDS = [

    "GLDRUB_TOM",

    "SLVRUB_TOM",

    "PLTRUB_TOM",

    "PLDRUB_TOM",

]



# ------------------------------------------------------
# Таймфрейм MOEX
#
# 1  - минута
# 10 - 10 минут
# 60 - час
# 24 - день
# ------------------------------------------------------

INTERVAL = 10



limiter = RateLimiter(
    max_requests=3
)



all_metals = []



logger.info(
    "START RUN M10 METAL"
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


    metal_service = MetalService(

        candle_service

    )



    for secid in SECIDS:


        logger.info(
            "LOAD MOEX M10 SECID=%s",
            secid,
        )



        limiter.wait()



        prices = metal_service.get_prices(

            secid=secid,

            date_from=DATE_FROM,

            date_till=DATE_TO,

            interval=INTERVAL,

        )



        logger.info(
            "RECEIVED M10 DATA SECID=%s COUNT=%s",
            secid,
            len(prices),
        )



        all_metals.extend(
            prices
        )





# ------------------------------------------------------
# Сортировка
# ------------------------------------------------------

all_metals.sort(

    key=lambda x: (

        x.ticker,

        x.date,

    )

)



logger.info(
    "TOTAL M10 DATA ROWS=%s",
    len(all_metals),
)





# ------------------------------------------------------
# ClickHouse
# ------------------------------------------------------

if all_metals:


    logger.info(
        "START CLICKHOUSE INSERT M10 METAL"
    )



    with ClickHouseClient() as client:


        metal_clickhouse = MetalClickHouse(

            client,

            table_name="moex_api.moex_metal_m10"

        )



        writer = MetalM10WriterClickHouse(

            metal_clickhouse

        )



        writer.write(

            all_metals

        )



    logger.info(
        "CLICKHOUSE INSERT M10 METAL COMPLETE"
    )



else:


    logger.warning(
        "NO DATA RECEIVED FOR M10 METAL"
    )





logger.info(
    "M10 RUN COMPLETE"
)