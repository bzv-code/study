from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class FuturesModel(BaseModel):
    """
    Модель фьючерса MOEX ISS.

    Используется:

    - FuturesCatalog
    - FuturesService
    - FuturesClickHouse
    - аналитика фьючерсов

    Источник данных:

        MOEX ISS

    Endpoint:

        /iss/engines/futures/markets/forts/securities.json
    """

    model_config = ConfigDict(
        extra="ignore"
    )

    # --------------------------------------------------
    # Идентификаторы
    # --------------------------------------------------

    secid: str = ""

    engine: str = "futures"

    market: str = "forts"

    board: str = ""

    # --------------------------------------------------
    # Названия
    # --------------------------------------------------

    shortname: str = ""

    secname: str = ""

    latname: str = ""

    # --------------------------------------------------
    # Базовый актив
    # --------------------------------------------------

    asset_code: str = ""

    underlying_asset: str = ""

    # --------------------------------------------------
    # Тип инструмента
    # --------------------------------------------------

    sectype: str = ""

    # --------------------------------------------------
    # Расчетные цены
    # --------------------------------------------------

    prev_settle_price: float = 0.0

    last_settle_price: float = 0.0

    settle_price_clr: float = 0.0

    prev_price: float = 0.0

    # --------------------------------------------------
    # Торговые параметры
    # --------------------------------------------------

    decimals: int = 0

    min_step: float = 0.0

    step_price: float = 0.0

    lot_volume: int = 0

    # --------------------------------------------------
    # Лимиты цены
    # --------------------------------------------------

    high_limit: float = 0.0

    low_limit: float = 0.0

    # --------------------------------------------------
    # Маржинальные параметры
    # --------------------------------------------------

    initial_margin: float = 0.0

    # --------------------------------------------------
    # Открытый интерес
    # --------------------------------------------------

    prev_open_position: int = 0

    # --------------------------------------------------
    # Даты
    # --------------------------------------------------

    last_trade_date: date | None = None

    last_delivery_date: date | None = None

    expiration_date: date | None = None

    # --------------------------------------------------
    # Время обновления
    # --------------------------------------------------

    im_time: datetime | None = None

    # --------------------------------------------------
    # Комиссии
    # --------------------------------------------------

    buy_sell_fee: float = 0.0

    scalper_fee: float = 0.0

    negotiated_fee: float = 0.0

    exercise_fee: float = 0.0