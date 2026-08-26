from __future__ import annotations

import os
import json
import signal
import calendar
from typing import Set

from client.moex_client import MoexClient
from catalog.stock_catalog import StockCatalog
from services.stock_service import StockService
from services.stock_candle_service import StockCandleService
from services.sector_service import SectorService
from utils.rate_limiter import RateLimiter
from utils.logger import get_logger
from database.client_clickhouse import ClickHouseClient
from database.stock.stock_clickhouse import StockClickHouse
from database.stock.writer_stock_m1_clickhouse import StockM1WriterClickHouse

logger = get_logger(__name__)

# ======================================================
# PERIOD
# ======================================================

YEAR = 2011
MONTH = 5

# Автоматический расчет дат начала и конца месяца
DATE_FROM = f"{YEAR}-{MONTH:02d}-01"
_, last_day = calendar.monthrange(YEAR, MONTH)
DATE_TO = f"{YEAR}-{MONTH:02d}-{last_day:02d}"

# минутные свечи
INTERVAL = 1

SECIDS = [
    #Энергетические и минеральные ресурсы
    "ROSN", "LKOH", "GAZP", "SIBN", "TATN", "SNGS", "BANE", "RASP", "VJGZ", "VJGZP",
    "JNOS", "MFGS", "UKUZ", "RNFT", "KRKN", "KRKNP", "BLNG", "SNGSP", "MFGSP", "TATNP",
    "JNOSP", "BANEP", "NVTK", "GAZA", "GAZAP", "GAZC", "GAZS", "GAZT", "TRNFP", "UGLD",
    #Финансы
    "SBER", "VTBR", "DOMRF", "PIKK", "MOEX", "CBOM", "BSPB", "RGSS", "KFBA", "POSI",
    "LSRG", "AVAN", "USBN", "RENI", "MBNK", "SFIN", "WTCM", "SPBE", "SMLT", "PRMB",
    "CHGZ", "RDRB", "ARSA", "KUZB", "RTKMP", "WTCMP", "BSPBP", "SBERP", "T", "LEAS",
    "MGKL", "ZAYM",
    #Несырьевые полезные ископаемые
    "GMKN", "PLZL", "CHMF", "NLMK", "RUAL", "VSMO", "MAGN", "ENPG", "ALRS", "TRMK",
    "SELG", "MTLR", "MTLRP", "URKZ", "CHMK", "BRZL", "ROLO", "KOGK", "IGST", "IGSTP",
    "UNKL", "EVRZ", "AMEZ", "MGNZ", "LNZL", "LNZLP",
    #Связь
    "MTSS", "RTKM", "MGTS", "AFKS", "TTLK", "NSVZ", "CNTL", "CNTLP", "RTKMP", "MGTSP", "BISVP",
    #Технологии
    "OZON", "VKCO", "RBCM", "ASTR", "DATA", "HEAD", "SOFL", "YDEX",
    #Транспорт
    "FESH", "FLOT", "AFLT", "NMTP", "UTAR", "NKHP", "GTRK", "TUZA", "MTPV", "SEMP",
    "VFLT", "VMTP", "URAL", "ZHDY", "NOMP", "WUSH",
    #Розничная торговля
    "LENT", "MGNT", "APTK", "OKEY", "MVID", "X5",
    #Здравоохранение
    "ABIO", "GEMA", "OZPH", "MDMG",
    #Медицинские технологии
    "DIOD", "LIFE", "DIAS",
    #Потребительские услуги
    "ROST",
    #Коммерческие услуги
    "GRNT", "SVET", "SVETP",
    #Электроэнергетика
    "ASSB", "DVEC", "EELT", "FEES", "HYDR", "IRAO", "IRKT", "KCHE", "KCHEP", "KLSB",
    "LPSB", "LSNG", "LSNGP", "MRKC", "MRKK", "MRKP", "MRKS", "MRKU", "MRKV", "MRKY",
    "MRKZ", "MRSB", "MSNG", "MSRS", "NNSB", "NNSBP", "OGKB", "OMZZP", "PMSB", "PMSBP",
    "RTGZ", "RTSB", "RTSBP", "RZSB", "SARE", "SAREP", "STSB", "STSBP", "TASB", "TASBP",
    "TGKA", "TGKB", "TGKBP", "TGKN", "TNSE", "VGSB", "VGSBP", "VRSB", "VRSBP", "YRSB", "YRSBP",
    #Химическая промышленность
    "AKRN", "HIMCP", "KAZT", "KAZTP", "KZOS", "KZOSP", "PHOR",
    #Потребительские товары
    "ABRD", "AQUA", "BELU", "GCHE",
    #Машиностроение
    "CHKZ", "KMAZ", "NFAZ", "RKKE", "SVAV", "UNAC", "ZILL",
    #Строительство
    "APRI", "BAZA", "CARM", "MSTT",
    #Лесная промышленность
    "SGZH",
    #Прочее
    "BTBR", "CNRU", "DELI", "DZRD", "DZRDP", "ELFV", "ELMT", "ETLN", "EUTR", "FIXR",
    "GECO", "GEMC", "GLRX", "HNFG", "INCB", "IVAT", "KBSB", "KGKC", "KGKCP", "KLVZ",
    "KMEZ", "KRKOP", "KROT", "KROTP", "LMBZ", "LVHK", "MAGE", "MAGEP", "MISB", "MISBP",
    "NAUK", "NKNC", "NKNCP", "NKSH", "PAZA", "PRFN", "PRMD", "RAGR", "RUSI", "SAGO",
    "SAGOP", "SLEN", "SVCB", "TORS", "TORSP", "UPRO", "UWGN", "VLHZ", "VSEH", "VSYD",
    "VSYDP", "YAKG", "YKEN", "YKENP", "ZVEZ",
]

# ======================================================
# CHECKPOINT (для возможности остановки и продолжения)
# ======================================================

CHECKPOINT_FILE = f"checkpoint_stock_m1_{YEAR}_{MONTH:02d}.json"

def load_checkpoint() -> Set[str]:
    if os.path.exists(CHECKPOINT_FILE):
        try:
            with open(CHECKPOINT_FILE, 'r', encoding='utf-8') as f:
                return set(json.load(f))
        except Exception as e:
            logger.warning("Не удалось прочитать файл checkpoint, начинаем сначала: %s", e)
            return set()
    return set()

def save_checkpoint(checkpoint: Set[str]):
    try:
        with open(CHECKPOINT_FILE, 'w', encoding='utf-8') as f:
            json.dump(list(checkpoint), f, indent=2)
    except Exception as e:
        logger.error("Не удалось сохранить checkpoint: %s", e)

checkpoint = load_checkpoint()

# ======================================================
# ОБРАБОТКА СИГНАЛОВ ОСТАНОВКИ (Ctrl+C)
# ======================================================

stop_requested = False

def signal_handler(signum, frame):
    global stop_requested
    logger.warning("Получен сигнал остановки (например, Ctrl+C). Скрипт завершит текущую итерацию и корректно остановится.")
    stop_requested = True

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# ======================================================
# INIT
# ======================================================

limiter = RateLimiter(max_requests=3)

logger.info("START RUN STOCK M1")
logger.info("DATE FROM=%s DATE TO=%s INTERVAL=%s", DATE_FROM, DATE_TO, INTERVAL)
logger.info("SECIDS COUNT=%s", len(SECIDS))
logger.info("ALREADY PROCESSED COUNT=%s", len(checkpoint))

# ======================================================
# MOEX & CLICKHOUSE
# ======================================================

with MoexClient() as client:
    logger.info("MOEX CLIENT CREATED")

    stock_catalog = StockCatalog(client)
    stock_service = StockService(stock_catalog)
    sector_service = SectorService()
    candle_service = StockCandleService(client, stock_service)

    # Открываем соединение с ClickHouse один раз на весь процесс для эффективности
    with ClickHouseClient() as ch_client:
        stock_clickhouse = StockClickHouse(ch_client, table_name="moex_api.moex_stock_m1")
        writer = StockM1WriterClickHouse(stock_clickhouse)

        for secid in SECIDS:
            # Проверка флага остановки
            if stop_requested:
                logger.info("ОСТАНОВКА ЗАПРОШЕНА. Завершаем работу.")
                break

            # Пропуск уже обработанных тикеров
            if secid in checkpoint:
                logger.info("SKIP ALREADY PROCESSED SECID=%s", secid)
                continue

            logger.info("LOAD STOCK SECID=%s", secid)
            limiter.wait()

            try:
                stock = stock_service.get(secid)
                stock = sector_service.enrich(stock)

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

                logger.info("CANDLES RECEIVED SECID=%s COUNT=%s", secid, len(candles))

                # Сразу записываем данные в ClickHouse (надежнее и экономит память)
                writer.write(stock, candles)
                logger.info("CLICKHOUSE INSERTED SECID=%s", secid)

                # Обновляем checkpoint только после успешной обработки и записи
                checkpoint.add(secid)
                save_checkpoint(checkpoint)
                logger.info("CHECKPOINT UPDATED SECID=%s", secid)

            except Exception as error:
                logger.exception("STOCK LOAD ERROR SECID=%s ERROR=%s", secid, error)

logger.info("RUN COMPLETE STOCK M1")
logger.info("TOTAL PROCESSED IN THIS RUN=%s", len(checkpoint))