from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator

from utils.datetime_utils import parse_moscow_datetime



class CandleModel(BaseModel):
    """
    Универсальная модель свечи MOEX ISS.

    Используется:

    - акции
    - металлы
    - валюты
    - минутные свечи m1
    - дневные свечи d1


    Время:

        Europe/Moscow
    """


    model_config = ConfigDict(
        extra="ignore"
    )



    # --------------------------------------------------
    # Информация об инструменте
    # --------------------------------------------------

    secid: str = ""

    ticker: str = ""

    name: str = ""

    engine: str = ""

    market: str = ""

    board: str = ""



    # --------------------------------------------------
    # Время свечи
    # --------------------------------------------------

    begin: datetime | None = None

    end: datetime | None = None



    # --------------------------------------------------
    # OHLC
    # --------------------------------------------------

    open: float = 0.0

    high: float = 0.0

    low: float = 0.0

    close: float = 0.0



    # --------------------------------------------------
    # Объемы
    # --------------------------------------------------

    volume: int = 0

    value: float = 0.0



    # --------------------------------------------------
    # Нормализация времени MOEX
    # --------------------------------------------------

    @field_validator(
        "begin",
        "end",
        mode="before",
    )
    @classmethod
    def validate_datetime(
        cls,
        value,
    ) -> datetime | None:
        """
        Все даты приводим
        к московскому времени.
        """


        if value in (
            None,
            "",
        ):

            return None


        return parse_moscow_datetime(
            value
        )