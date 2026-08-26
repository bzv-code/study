from __future__ import annotations


from client.moex_client import MoexClient


from services.dividend_service import (
    DividendService,
)


from utils.rate_limiter import (
    RateLimiter,
)


from utils.logger import (
    get_logger,
)



from database.client_clickhouse import (
    ClickHouseClient,
)


from database.dividend.dividend_clickhouse import (
    DividendClickHouse,
)


from database.dividend.writer_dividend_clickhouse import (
    DividendWriterClickHouse,
)







logger = get_logger(__name__)








# ======================================================
# SECIDS
# ======================================================


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
    "JNOS",
    "MFGS",
    "UKUZ",
    "RNFT",
    "KRKN",
    "BLNG",
    "SNGSP",
    "MFGSP",
    "TATNP",
    "JNOSP",
    "NVTK",

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
    "URKZ",
    "CHMK",
    "BRZL",
    "ROLO",
    "KOGK",
    "IGST",
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
    "RTKMP",
    "MGTSP",
    "BISVP",

    #Технологии

    "OZON",
    "VKCO",
    "RBCM",

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

    #Розничная торговля

    "LENT",
    "MGNT",
    "APTK",
    "OKEY",

    #Здравоохранение

    "ABIO",
    "GEMA",

    #Медицинские технологии

    "DIOD",
    "LIFE",

    #Потребительские услуги

    "ROST",

    #Коммерческие услуги

    "GRNT",
    "SVET"

]









limiter = RateLimiter(

    max_requests=3

)








logger.info(

    "START RUN DIVIDENDS"

)



logger.info(

    "SECIDS COUNT=%s",

    len(SECIDS),

)









dividends_data = []









# ======================================================
# MOEX
# ======================================================


with MoexClient() as client:



    logger.info(

        "MOEX CLIENT CREATED"

    )





    dividend_service = DividendService(

        client

    )








    for secid in SECIDS:



        logger.info(

            "LOAD DIVIDENDS SECID=%s",

            secid,

        )




        limiter.wait()





        try:




            dividends = dividend_service.get(

                secid

            )






            logger.info(

                "DIVIDENDS RECEIVED SECID=%s COUNT=%s",

                secid,

                len(dividends),

            )







            if dividends:


                dividends_data.extend(

                    dividends

                )







        except Exception as error:



            logger.exception(

                "DIVIDENDS LOAD ERROR SECID=%s ERROR=%s",

                secid,

                error,

            )













logger.info(

    "TOTAL DIVIDENDS READY=%s",

    len(dividends_data),

)













# ======================================================
# CLICKHOUSE
# ======================================================


if dividends_data:



    logger.info(

        "START CLICKHOUSE INSERT"

    )





    with ClickHouseClient() as client:




        dividend_clickhouse = DividendClickHouse(



            client,

            table_name="moex_api.moex_stock_dividends"



        )







        writer = DividendWriterClickHouse(



            dividend_clickhouse



        )







        writer.write(

            dividends_data

        )







    logger.info(

        "CLICKHOUSE INSERT FINISHED"

    )






else:



    logger.warning(

        "NO DIVIDENDS DATA RECEIVED"

    )









logger.info(

    "RUN COMPLETE DIVIDENDS"

)