from __future__ import annotations


from client.moex_client import MoexClient


from catalog.stock_catalog import StockCatalog


from services.stock_service import StockService
from services.stock_candle_service import StockCandleService
from services.sector_service import SectorService


from utils.rate_limiter import RateLimiter
from utils.logger import get_logger


from database.client_clickhouse import ClickHouseClient


from database.stock.stock_clickhouse import (
    StockClickHouse,
)


from database.stock.writer_stock_h_clickhouse import (
    StockHWriterClickHouse,
)



logger = get_logger(__name__)





# ======================================================
# PERIOD
# ======================================================


DATE_FROM = "2000-01-01"

DATE_TO = "2026-07-31"



# недельные свечи

INTERVAL = 7





SECIDS = [

    #Энергетические и минеральные ресурсы
    "ROSN",
    "LKOH",
    "GAZP",
    "SIBN",
    "TATN",
    "SNGS",
    "BANE",
    "RASP",
    "VJGZ",
    "VJGZP",
    "JNOS",
    "MFGS",
    "UKUZ",
    "RNFT",
    "KRKN",
    "KRKNP",
    "BLNG",
    "SNGSP",
    "MFGSP",
    "TATNP",
    "JNOSP",
    "BANEP",
    "NVTK",
    "GAZA",
    "GAZAP",
    "GAZC",
    "GAZS",
    "GAZT",
    "TRNFP",
    "UGLD",

    #Финансы
    "SBER",
    "VTBR",
    "DOMRF",
    "PIKK",
    "MOEX",
    "CBOM",
    "BSPB",
    "RGSS",
    "KFBA",
    "POSI",
    "LSRG",
    "AVAN",
    "USBN",
    "RENI",
    "MBNK",
    "SFIN",
    "WTCM",
    "SPBE",
    "SMLT",
    "PRMB",
    "CHGZ",
    "RDRB",
    "ARSA",
    "KUZB",
    "RTKMP",
    "WTCMP",
    "BSPBP",
    "SBERP",
    "T",
    "LEAS",
    "MGKL",
    "ZAYM",

    #Несырьевые полезные ископаемые
    "GMKN",
    "PLZL",
    "CHMF",
    "NLMK",
    "RUAL",
    "VSMO",
    "MAGN",
    "ENPG",
    "ALRS",
    "TRMK",
    "SELG",
    "MTLR",
    "MTLRP",
    "URKZ",
    "CHMK",
    "BRZL",
    "ROLO",
    "KOGK",
    "IGST",
    "IGSTP",
    "UNKL",
    "EVRZ",
    "AMEZ",
    "MGNZ",
    "LNZL",
    "LNZLP",

    #Связь
    "MTSS",
    "RTKM",
    "MGTS",
    "AFKS",
    "TTLK",
    "NSVZ",
    "CNTL",
    "CNTLP",
    "MGTSP",
    "BISVP",

    #Технологии
    "OZON",
    "VKCO",
    "RBCM",
    "ASTR",
    "DATA",
    "HEAD",
    "SOFL",
    "YDEX",

    #Транспорт
    "FESH",
    "FLOT",
    "AFLT",
    "NMTP",
    "UTAR",
    "NKHP",
    "GTRK",
    "TUZA",
    "MTPV",
    "SEMP",
    "VFLT",
    "VMTP",
    "URAL",
    "ZHDY",
    "NOMP",
    "WUSH",

    #Розничная торговля
    "LENT",
    "MGNT",
    "APTK",
    "OKEY",
    "MVID",
    "X5",

    #Здравоохранение
    "ABIO",
    "GEMA",
    "OZPH",
    "MDMG",

    #Медицинские технологии
    "DIOD",
    "LIFE",
    "DIAS",

    #Потребительские услуги
    "ROST",

    #Коммерческие услуги
    "GRNT",
    "SVET",
    "SVETP",

    #Электроэнергетика
    "ASSB",
    "DVEC",
    "EELT",
    "FEES",
    "HYDR",
    "IRAO",
    "IRKT",
    "KCHE",
    "KCHEP",
    "KLSB",
    "LPSB",
    "LSNG",
    "LSNGP",
    "MRKC",
    "MRKK",
    "MRKP",
    "MRKS",
    "MRKU",
    "MRKV",
    "MRKY",
    "MRKZ",
    "MRSB",
    "MSNG",
    "MSRS",
    "NNSB",
    "NNSBP",
    "OGKB",
    "OMZZP",
    "PMSB",
    "PMSBP",
    "RTGZ",
    "RTSB",
    "RTSBP",
    "RZSB",
    "SARE",
    "SAREP",
    "STSB",
    "STSBP",
    "TASB",
    "TASBP",
    "TGKA",
    "TGKB",
    "TGKBP",
    "TGKN",
    "TNSE",
    "VGSB",
    "VGSBP",
    "VRSB",
    "VRSBP",
    "YRSB",
    "YRSBP",

    #Химическая промышленность
    "AKRN",
    "HIMCP",
    "KAZT",
    "KAZTP",
    "KZOS",
    "KZOSP",
    "PHOR",

    #Потребительские товары
    "ABRD",
    "AQUA",
    "BELU",
    "GCHE",

    #Машиностроение
    "CHKZ",
    "KMAZ",
    "NFAZ",
    "RKKE",
    "SVAV",
    "UNAC",
    "ZILL",

    #Строительство
    "APRI",
    "BAZA",
    "CARM",
    "MSTT",

    #Лесная промышленность
    "SGZH",

    #Прочее
    "BTBR",
    "CNRU",
    "DELI",
    "DZRD",
    "DZRDP",
    "ELFV",
    "ELMT",
    "ETLN",
    "EUTR",
    "FIXR",
    "GECO",
    "GEMC",
    "GLRX",
    "HNFG",
    "INCB",
    "IVAT",
    "KBSB",
    "KGKC",
    "KGKCP",
    "KLVZ",
    "KMEZ",
    "KRKOP",
    "KROT",
    "KROTP",
    "LMBZ",
    "LVHK",
    "MAGE",
    "MAGEP",
    "MISB",
    "MISBP",
    "NAUK",
    "NKNC",
    "NKNCP",
    "NKSH",
    "PAZA",
    "PRFN",
    "PRMD",
    "RAGR",
    "RUSI",
    "SAGO",
    "SAGOP",
    "SLEN",
    "SVCB",
    "TORS",
    "TORSP",
    "UPRO",
    "UWGN",
    "VLHZ",
    "VSEH",
    "VSYD",
    "VSYDP",
    "YAKG",
    "YKEN",
    "YKENP",
    "ZVEZ",

]





limiter = RateLimiter(

    max_requests=3

)





logger.info(
    "START RUN STOCK H"
)


logger.info(
    "DATE FROM=%s DATE TO=%s INTERVAL=%s",
    DATE_FROM,
    DATE_TO,
    INTERVAL,
)



logger.info(
    "SECIDS COUNT=%s",
    len(SECIDS),
)





stocks_data = []





# ======================================================
# MOEX
# ======================================================


with MoexClient() as client:


    logger.info(
        "MOEX CLIENT CREATED"
    )


    stock_catalog = StockCatalog(
        client
    )


    stock_service = StockService(
        stock_catalog
    )


    sector_service = SectorService()



    candle_service = StockCandleService(
        client,
        stock_service,
    )





    for secid in SECIDS:


        logger.info(
            "LOAD STOCK SECID=%s",
            secid,
        )


        limiter.wait()



        try:


            stock = stock_service.get(
                secid
            )



            stock = sector_service.enrich(
                stock
            )



            logger.info(
                """
STOCK INFO

SECID=%s
ISIN=%s
SECTOR=%s
BOARD=%s
""",

                stock.secid,
                stock.isin,
                stock.sector,
                stock.board,

            )





            candles = candle_service.get(

                secid=secid,

                date_from=DATE_FROM,

                date_till=DATE_TO,

                interval=INTERVAL,

            )





            logger.info(

                "CANDLES RECEIVED SECID=%s COUNT=%s",

                secid,

                len(candles),

            )




            stocks_data.append(

                (

                    stock,

                    candles,

                )

            )



        except Exception as error:


            logger.exception(

                "STOCK LOAD ERROR SECID=%s ERROR=%s",

                secid,

                error,

            )









logger.info(

    "TOTAL STOCKS READY=%s",

    len(stocks_data),

)








# ======================================================
# CLICKHOUSE
# ======================================================


if stocks_data:



    logger.info(

        "START CLICKHOUSE INSERT"

    )




    with ClickHouseClient() as client:



        stock_clickhouse = StockClickHouse(


            client,

            table_name="moex_api.moex_stock_h",


        )




        writer = StockHWriterClickHouse(


            stock_clickhouse,

        )





        for stock, candles in stocks_data:



            writer.write(

                stock,

                candles,

            )






    logger.info(

        "CLICKHOUSE INSERT FINISHED"

    )



else:



    logger.warning(

        "NO STOCK DATA RECEIVED"

    )








logger.info(

    "RUN COMPLETE STOCK H"

)