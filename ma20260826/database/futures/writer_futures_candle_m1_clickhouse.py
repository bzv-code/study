
from __future__ import annotations

from datetime import datetime
from typing import Any

from models.futures_model import FuturesModel
from models.candle_model import CandleModel

from database.futures.futures_clickhouse import (
    FuturesClickHouse,
)

from database.duplicate_checker_clickhouse import (
    DuplicateCheckerClickHouse,
)

from utils.datetime_utils import (
    parse_moscow_datetime,
)

from utils.logger import get_logger


logger = get_logger(__name__)


# ======================================================
# SECTORS
# ======================================================

FUTURES_SECTORS = {

    # --------------------------------------------------
    # Валюта
    # --------------------------------------------------

    "CNYRUBF": "Currency",

    "EURRUBF": "Currency",

    "USDRUBF": "Currency",


    # --------------------------------------------------
    # Индексы
    # --------------------------------------------------

    "IMOEXF": "Index",

    "RGBIF": "Index",


    # --------------------------------------------------
    # Металлы
    # --------------------------------------------------

    "GLDRUBF": "Precious_Metals",

    "SLVRUBF": "Precious_Metals",


    # --------------------------------------------------
    # Акции
    # --------------------------------------------------

    "GAZPF": "Stocks",

    "SBERF": "Stocks",

}


# ======================================================
# WRITER
# ======================================================

class FuturesCandleM1WriterClickHouse:
    """
    Загрузчик минутных свечей бессрочных фьючерсов MOEX
    в ClickHouse.

    Таблица:

        moex_api.moex_futures_candle_m1


    Источник:

        FuturesModel
        CandleModel


    Таймфрейм:

        interval=1


    Проверка дублей:

        secid + date


    Поля ClickHouse:

        secid
        board
        asset_code
        sector
        date
        open
        high
        low
        close
        volume
        value


    Сектор:

        Передаётся из run_futures_candle_m1.py.

        Если sector не передан, используется
        локальный словарь FUTURES_SECTORS.


    ВАЖНО:

        Значение sector сохраняется в ClickHouse
        точно в том виде, в котором оно указано
        в FUTURES_SECTORS.

        Никакого .lower() или .upper()
        для sector не выполняется.
    """

    TABLE_NAME = (
        "moex_api.moex_futures_candle_m1"
    )

    BATCH_SIZE = 5000


    # --------------------------------------------------
    # Колонки ClickHouse
    # --------------------------------------------------

    COLUMNS = [

        "secid",

        "board",

        "asset_code",

        "sector",

        "date",

        "open",

        "high",

        "low",

        "close",

        "volume",

        "value",

    ]


    # --------------------------------------------------
    # Ключ проверки дублей
    # --------------------------------------------------

    KEY_COLUMNS = [

        "secid",

        "date",

    ]


    # ==================================================
    # INIT
    # ==================================================

    def __init__(
        self,
        clickhouse: FuturesClickHouse,
    ) -> None:

        self.clickhouse = clickhouse

        self.duplicate_checker = (
            DuplicateCheckerClickHouse(

                clickhouse.client

            )
        )

        logger.debug(

            "FuturesCandleM1WriterClickHouse "
            "initialized TABLE=%s",

            self.TABLE_NAME,

        )


    # ==================================================
    # SECTOR
    # ==================================================

    @staticmethod
    def _get_sector(
        secid: str,
    ) -> str:
        """
        Возвращает сектор фьючерса.

        Сектор определяется по SECID
        из FUTURES_SECTORS.

        Значение возвращается без изменения
        регистра.
        """

        normalized_secid = str(
            secid or ""
        ).strip().upper()


        sector = FUTURES_SECTORS.get(
            normalized_secid
        )


        if not sector:

            raise ValueError(

                f"Сектор для фьючерса "
                f"'{normalized_secid}' не задан "
                f"в FUTURES_SECTORS"

            )


        return sector


    # ==================================================
    # DATETIME
    # ==================================================

    @staticmethod
    def _parse_date(
        value: datetime | None,
    ) -> datetime | None:
        """
        Приведение времени MOEX
        к Europe/Moscow.

        Для M1 сохраняется
        минутная точность timestamp.
        """

        if value is None:

            return None


        return parse_moscow_datetime(
            value
        )


    # ==================================================
    # PREPARE ROW
    # ==================================================

    def _prepare_row(
        self,
        future: FuturesModel,
        candle: CandleModel,
        sector: str,
    ) -> list[Any]:
        """
        FuturesModel + CandleModel + sector
        ->
        строка ClickHouse.
        """

        logger.debug(

            "PREPARE FUTURES CANDLE M1 ROW "
            "SECID=%s SECTOR=%s DATE=%s",

            future.secid,

            sector,

            candle.begin,

        )


        candle_date = self._parse_date(
            candle.begin
        )


        if candle_date is None:

            raise ValueError(

                f"Некорректная дата свечи "
                f"SECID={future.secid}"

            )


        return [

            # ------------------------------------------
            # Идентификатор
            # ------------------------------------------

            future.secid,


            # ------------------------------------------
            # Торговая доска
            # ------------------------------------------

            future.board,


            # ------------------------------------------
            # Базовый актив
            # ------------------------------------------

            future.asset_code,


            # ------------------------------------------
            # Сектор
            # ------------------------------------------

            sector,


            # ------------------------------------------
            # Время свечи
            # ------------------------------------------

            candle_date,


            # ------------------------------------------
            # OHLC
            # ------------------------------------------

            candle.open,

            candle.high,

            candle.low,

            candle.close,


            # ------------------------------------------
            # Объемы
            # ------------------------------------------

            candle.volume,

            candle.value,

        ]


    # ==================================================
    # WRITE
    # ==================================================

    def write(
        self,
        future: FuturesModel,
        candles: list[CandleModel],
        sector: str | None = None,
    ) -> None:
        """
        Запись минутных свечей фьючерса
        чанками в ClickHouse.

        Parameters
        ----------
        future:
            Информация о фьючерсе.

        candles:
            Список минутных свечей.

        sector:
            Сектор фьючерса.

            Если передан из
            run_futures_candle_m1.py,
            используется именно это значение.

            Если None, сектор определяется
            через FUTURES_SECTORS.

        ВАЖНО:

            Регистр sector сохраняется
            без изменений.
        """

        if not candles:

            logger.warning(

                "NO FUTURES M1 CANDLES FOR INSERT "
                "TABLE=%s SECID=%s",

                self.TABLE_NAME,

                future.secid,

            )


            print(
                "NO DATA FOR INSERT"
            )


            return


        # ==================================================
        # НОРМАЛИЗАЦИЯ / ОПРЕДЕЛЕНИЕ СЕКТОРА
        # ==================================================

        if sector is None:

            sector = self._get_sector(
                future.secid
            )

        else:

            # --------------------------------------------------
            # ВАЖНО:
            #
            # НЕ используем .lower()
            # НЕ используем .upper()
            #
            # Сохраняем переданный sector
            # именно в том виде, как его указал
            # вызывающий код.
            # --------------------------------------------------

            sector = str(
                sector
            ).strip()


            if not sector:

                raise ValueError(

                    f"Пустой sector "
                    f"SECID={future.secid}"

                )


        # ==================================================
        # START
        # ==================================================

        logger.info(

            "CLICKHOUSE FUTURES M1 CANDLES "
            "INSERT START TABLE=%s "
            "SECID=%s SECTOR=%s INPUT=%s",

            self.TABLE_NAME,

            future.secid,

            sector,

            len(candles),

        )


        print("=" * 80)

        print(
            "CLICKHOUSE INSERT FUTURES CANDLE M1"
        )

        print("=" * 80)


        print(
            f"SECID : {future.secid}"
        )

        print(
            f"ASSET : {future.asset_code}"
        )

        print(
            f"BOARD : {future.board}"
        )

        print(
            f"SECTOR: {sector}"
        )

        print(
            f"INPUT ROWS: {len(candles)}"
        )

        print()


        # ==================================================
        # PREPARE ROWS
        # ==================================================

        rows = [

            self._prepare_row(

                future,

                candle,

                sector,

            )

            for candle in candles

        ]


        logger.debug(

            "FUTURES M1 CANDLE ROWS PREPARED "
            "SECID=%s SECTOR=%s COUNT=%s",

            future.secid,

            sector,

            len(rows),

        )


        print(
            f"ROWS PREPARED: {len(rows)}"
        )


        # ==================================================
        # EXISTING KEYS
        # ==================================================

        existing_keys = (
            self.duplicate_checker.load_existing_keys(

                table=self.TABLE_NAME,

                key_columns=self.KEY_COLUMNS,

            )
        )


        logger.debug(

            "EXISTING FUTURES M1 CANDLE KEYS "
            "SECID=%s COUNT=%s",

            future.secid,

            len(existing_keys),

        )


        # ==================================================
        # DUPLICATE CHECK
        # ==================================================

        rows = (
            self.duplicate_checker.filter_new_rows(

                rows=rows,

                columns=self.COLUMNS,

                existing_keys=existing_keys,

                key_columns=self.KEY_COLUMNS,

            )
        )


        logger.info(

            "FUTURES M1 CANDLE ROWS AFTER "
            "DUPLICATE CHECK "
            "SECID=%s SECTOR=%s COUNT=%s",

            future.secid,

            sector,

            len(rows),

        )


        print(

            "ROWS AFTER DUPLICATE CHECK: "
            f"{len(rows)}"

        )


        if not rows:

            print()

            print(
                "NOTHING TO INSERT"
            )

            print("=" * 80)

            return


        # ==================================================
        # INSERT BATCHES
        # ==================================================

        inserted = 0


        for start in range(

            0,

            len(rows),

            self.BATCH_SIZE,

        ):

            end = min(

                start + self.BATCH_SIZE,

                len(rows),

            )


            batch = rows[start:end]


            logger.debug(

                "INSERT FUTURES M1 CANDLE "
                "BATCH START=%s END=%s SIZE=%s "
                "SECID=%s SECTOR=%s",

                start,

                end,

                len(batch),

                future.secid,

                sector,

            )


            print(

                f"INSERT BATCH: "
                f"{start} - {end} "
                f"SIZE={len(batch)}"

            )


            try:

                self.clickhouse.insert(

                    data=batch,

                    columns=self.COLUMNS,

                )


            except Exception as error:

                logger.exception(

                    "CLICKHOUSE FUTURES M1 CANDLE "
                    "INSERT ERROR "
                    "TABLE=%s "
                    "SECID=%s "
                    "SECTOR=%s "
                    "ERROR=%s",

                    self.TABLE_NAME,

                    future.secid,

                    sector,

                    error,

                )

                raise


            inserted += len(batch)


        # ==================================================
        # COMPLETE
        # ==================================================

        logger.info(

            "CLICKHOUSE FUTURES M1 CANDLE "
            "INSERT COMPLETE "
            "TABLE=%s "
            "SECID=%s "
            "SECTOR=%s "
            "INSERTED=%s",

            self.TABLE_NAME,

            future.secid,

            sector,

            inserted,

        )


        print()

        print(
            f"INSERTED: {inserted}"
        )

        print(
            "STATUS: OK"
        )

        print("=" * 80)

