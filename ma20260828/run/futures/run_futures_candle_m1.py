
from __future__ import annotations

from client.moex_client import MoexClient

from catalog.futures_catalog import FuturesCatalog

from services.futures_service import FuturesService
from services.futures_candle_service import FuturesCandleService

from utils.rate_limiter import RateLimiter
from utils.logger import get_logger

from database.client_clickhouse import ClickHouseClient

from database.futures.futures_clickhouse import (
    FuturesClickHouse,
)

from database.futures.writer_futures_candle_m1_clickhouse import (
    FuturesCandleM1WriterClickHouse,
)


logger = get_logger(__name__)


# ======================================================
# SETTINGS
# ======================================================

DATE_FROM = "2010-01-01"

DATE_TO = "2026-07-31"

INTERVAL = 1

TABLE_NAME = (
    "moex_api.moex_futures_candle_m1"
)


# ======================================================
# PERPETUAL FUTURES
# ======================================================

PERPETUAL_FUTURES = {

    # --------------------------------------------------
    # Валюта
    # --------------------------------------------------

    "Валюта": [

        "CNYRUBF",

        "EURRUBF",

        "USDRUBF",

    ],


    # --------------------------------------------------
    # Индексы
    # --------------------------------------------------

    "Индексы": [

        "IMOEXF",

        "RGBIF",

    ],

    # --------------------------------------------------
    # Индексы иностранные
    # --------------------------------------------------

    "Индексы иностранные": [

        "SP500F",

        "QQQF",

    ],

    # --------------------------------------------------
    # Металлы
    # --------------------------------------------------

    "Металлы": [

        "GLDRUBF",

        "SLVRUBF",

    ],


    # --------------------------------------------------
    # Акции
    # --------------------------------------------------

    "Акции": [

        "GAZPF",

        "SBERF",

    ],

}


# ======================================================
# BUILD SECID -> SECTOR
# ======================================================

SECID_TO_SECTOR = {

    secid: sector

    for sector, secids in PERPETUAL_FUTURES.items()

    for secid in secids

}


SECIDS = list(

    SECID_TO_SECTOR.keys()

)


# ======================================================
# RATE LIMITER
# ======================================================

limiter = RateLimiter(

    max_requests=3

)


# ======================================================
# START
# ======================================================

logger.info(

    "START RUN FUTURES CANDLE M1"

)


logger.info(

    "DATE FROM=%s DATE TO=%s INTERVAL=%s",

    DATE_FROM,

    DATE_TO,

    INTERVAL,

)


logger.info(

    "TABLE=%s",

    TABLE_NAME,

)


logger.info(

    "PERPETUAL FUTURES COUNT=%s",

    len(SECIDS),

)


logger.info(

    "PERPETUAL FUTURES SECIDS=%s",

    ", ".join(SECIDS),

)


# ======================================================
# FUTURES DATA
# ======================================================

futures_data = []


# ======================================================
# MOEX
# ======================================================

with MoexClient() as client:

    logger.info(

        "MOEX CLIENT CREATED"

    )


    # --------------------------------------------------
    # Futures catalog
    # --------------------------------------------------

    futures_catalog = FuturesCatalog(

        client

    )


    # --------------------------------------------------
    # Futures service
    # --------------------------------------------------

    futures_service = FuturesService(

        futures_catalog

    )


    # --------------------------------------------------
    # Candle service
    # --------------------------------------------------

    candle_service = FuturesCandleService(

        client,

        futures_service,

    )


    # ==================================================
    # LOAD FUTURES
    # ==================================================

    for index, secid in enumerate(

        SECIDS,

        start=1,

    ):

        sector = SECID_TO_SECTOR.get(

            secid,

            "Other",

        )


        logger.info(

            "LOAD PERPETUAL FUTURE "
            "%s/%s SECID=%s SECTOR=%s",

            index,

            len(SECIDS),

            secid,

            sector,

        )


        # --------------------------------------------------
        # Rate limiter
        # --------------------------------------------------

        limiter.wait()


        try:

            # ----------------------------------------------
            # Find future
            # ----------------------------------------------

            future = futures_service.get(

                secid

            )


            logger.info(

                """
PERPETUAL FUTURES INFO

SECID=%s
SECTOR=%s
BOARD=%s
ASSET=%s
LOT=%s
LAST TRADE=%s
DELIVERY=%s
EXPIRATION=%s
""",

                future.secid,

                sector,

                future.board,

                future.asset_code,

                future.lot_volume,

                future.last_trade_date,

                future.last_delivery_date,

                future.expiration_date,

            )


            # ----------------------------------------------
            # Load M1 candles
            # ----------------------------------------------

            candles = candle_service.get(

                secid=secid,

                date_from=DATE_FROM,

                date_till=DATE_TO,

                interval=INTERVAL,

            )


            logger.info(

                "M1 CANDLES RECEIVED "
                "SECID=%s SECTOR=%s COUNT=%s",

                secid,

                sector,

                len(candles),

            )


            # ----------------------------------------------
            # Save data for ClickHouse
            # ----------------------------------------------

            futures_data.append(

                (

                    future,

                    candles,

                    sector,

                )

            )


            logger.info(

                "PERPETUAL FUTURE READY "
                "SECID=%s SECTOR=%s CANDLES=%s",

                secid,

                sector,

                len(candles),

            )


        except Exception as error:

            logger.exception(

                "FUTURES M1 LOAD ERROR "
                "SECID=%s SECTOR=%s ERROR=%s",

                secid,

                sector,

                error,

            )


# ======================================================
# MOEX COMPLETE
# ======================================================

logger.info(

    "TOTAL FUTURES M1 READY=%s",

    len(futures_data),

)


# ======================================================
# CLICKHOUSE
# ======================================================

if futures_data:

    logger.info(

        "START CLICKHOUSE M1 INSERT"

    )


    # --------------------------------------------------
    # ClickHouse client
    # --------------------------------------------------

    with ClickHouseClient() as client:

        logger.info(

            "CLICKHOUSE CLIENT CREATED"

        )


        # ----------------------------------------------
        # Futures ClickHouse
        # ----------------------------------------------

        futures_clickhouse = FuturesClickHouse(

            client,

            table_name=TABLE_NAME,

        )


        # ----------------------------------------------
        # Writer
        # ----------------------------------------------

        writer = FuturesCandleM1WriterClickHouse(

            futures_clickhouse

        )


        # ----------------------------------------------
        # Insert futures
        # ----------------------------------------------

        for future, candles, sector in futures_data:

            logger.info(

                "CLICKHOUSE WRITE M1 "
                "SECID=%s SECTOR=%s CANDLES=%s",

                future.secid,

                sector,

                len(candles),

            )


            writer.write(

                future,

                candles,

                sector,

            )


    logger.info(

        "CLICKHOUSE M1 INSERT FINISHED"

    )


else:

    logger.warning(

        "NO FUTURES M1 DATA RECEIVED"

    )


# ======================================================
# COMPLETE
# ======================================================

logger.info(

    "RUN COMPLETE FUTURES CANDLE M1"

)

