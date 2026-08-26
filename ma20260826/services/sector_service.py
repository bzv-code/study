from __future__ import annotations


from typing import TYPE_CHECKING


from utils.logger import get_logger


if TYPE_CHECKING:

    from models.stock_model import StockModel



logger = get_logger(__name__)




class SectorService:
    """
    Сервис определения сектора акций MOEX.

    Источник:

        внутренний SECTOR_MAP


    Заполняет:

        StockModel.sector


    Не изменяет:

        secid
        isin


    В будущем источник можно заменить:

        - Finam API
        - MOEX API
        - Excel
        - PostgreSQL
        - ClickHouse
    """



    SECTOR_UNKNOWN = "Неизвестно"



    SECTOR_MAP = {


        # --------------------------------------------------
        # Энергетика
        # --------------------------------------------------

        "Энергетические и минеральные ресурсы": [

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

        ],



        # --------------------------------------------------
        # Финансы
        # --------------------------------------------------

        "Финансы": [

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


        ],



        # --------------------------------------------------
        # Металлургия
        # --------------------------------------------------

        "Несырьевые полезные ископаемые": [

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


        ],



        # --------------------------------------------------
        # Связь
        # --------------------------------------------------

        "Связь": [

                "MTSS",
                "RTKM",
                "MGTS",
                "AFKS",
                "TTLK",
                "NSVZ",
                "CNTL",
                "CNTLP",
                "RTKMP",
                "MGTSP",
                "BISVP",

        ],



        # --------------------------------------------------
        # Технологии
        # --------------------------------------------------

        "Технологии": [

                "OZON",
                "VKCO",
                "RBCM",
                "ASTR",
                "DATA",
                "HEAD",
                "SOFL",
                "YDEX",

        ],



        # --------------------------------------------------
        # Транспорт
        # --------------------------------------------------

        "Транспорт": [

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

        ],



        # --------------------------------------------------
        # Ритейл
        # --------------------------------------------------

        "Розничная торговля": [

                "LENT",
                "MGNT",
                "APTK",
                "OKEY",
                "MVID",
                "X5",


        ],



        # --------------------------------------------------
        # Здравоохранение
        # --------------------------------------------------

        "Здравоохранение": [

                "ABIO",
                "GEMA",
                "OZPH",
                "MDMG",

        ],



        "Медицинские технологии": [

                "DIOD",
                "LIFE",
                "DIAS",

        ],



        "Потребительские услуги": [

            "ROST",

        ],



        "Коммерческие услуги": [

                "GRNT",
                "SVET",
                "SVETP",

        ],

        "Электроэнергетика": [

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

        ],

        "Химическая промышленность": [

                "AKRN",
                "HIMCP",
                "KAZT",
                "KAZTP",
                "KZOS",
                "KZOSP",
                "PHOR",

        ],

        "Потребительские товары": [

                "ABRD",
                "AQUA",
                "BELU",
                "GCHE",

        ],

        "Машиностроение": [

                "CHKZ",
                "KMAZ",
                "NFAZ",
                "RKKE",
                "SVAV",
                "UNAC",
                "ZILL",

        ],

        "Строительство": [

                "APRI",
                "BAZA",
                "CARM",
                "MSTT",

        ],

        "Лесная промышленность": [

                "SGZH",

        ],

        "Прочее": [

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

        ],

    }



    def __init__(self) -> None:

        logger.debug(
            "SectorService initialized"
        )




    def get_sector(
        self,
        ticker: str,
    ) -> str:
        """
        Возвращает сектор по тикеру.
        """


        if not ticker:

            return self.SECTOR_UNKNOWN



        ticker = ticker.upper().strip()



        for sector, tickers in self.SECTOR_MAP.items():


            if ticker in tickers:


                logger.debug(
                    "SECTOR FOUND TICKER=%s SECTOR=%s",
                    ticker,
                    sector,
                )


                return sector




        logger.debug(
            "SECTOR NOT FOUND TICKER=%s",
            ticker,
        )


        return self.SECTOR_UNKNOWN





    def enrich(
        self,
        stock: StockModel,
    ) -> StockModel:
        """
        Добавляет сектор в StockModel.
        """


        stock.sector = self.get_sector(
            stock.secid
        )


        return stock