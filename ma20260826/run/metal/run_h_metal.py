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

from database.metal.writer_metal_h_clickhouse import (
    MetalHWriterClickHouse,
)



logger = get_logger(__name__)




DATE_FROM = "2000-01-01"

DATE_TO = "2026-07-31"



SECIDS = [

    "GLDRUB_TOM",

    "SLVRUB_TOM",

    "PLTRUB_TOM",

    "PLDRUB_TOM",

]



# ------------------------------------------------------
# Таймфрейм MOEX ISS
#
# 1  - 1 минута
# 10 - 10 минут
# 60 - 1 час
# 24 - день
# 7  - неделя
#
# ------------------------------------------------------

INTERVAL = 7



limiter = RateLimiter(
    max_requests=3
)



all_metals = []




logger.info(
    "START METAL H RUN"
)

logger.info(
    "DATE FROM=%s DATE TO=%s INTERVAL=%s",
    DATE_FROM,
    DATE_TO,
    INTERVAL,
)



# ------------------------------------------------------
# Загрузка данных MOEX
# ------------------------------------------------------

with MoexClient() as client:


    logger.debug(
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


    metal_service = MetalService(

        candle_service

    )



    logger.debug(
        "SERVICES INITIALIZED"
    )



    for secid in SECIDS:


        logger.info(
            "LOAD MOEX H SECID=%s",
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
            "RECEIVED SECID=%s COUNT=%s",
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
    "TOTAL H DATA ROWS=%s",
    len(all_metals),
)






# ------------------------------------------------------
# ClickHouse
# ------------------------------------------------------

if all_metals:


    logger.info(
        "START CLICKHOUSE INSERT TABLE=moex_api.moex_metal_h"
    )


    with ClickHouseClient() as client:


        metal_clickhouse = MetalClickHouse(

            client,

            table_name="moex_api.moex_metal_h"

        )



        writer = MetalHWriterClickHouse(

            metal_clickhouse

        )



        writer.write(

            all_metals

        )


    logger.info(
        "CLICKHOUSE INSERT COMPLETE"
    )



else:


    logger.warning(
        "NO DATA RECEIVED"
    )






logger.info(
    "H RUN COMPLETE"
)