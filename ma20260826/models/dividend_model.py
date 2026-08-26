from __future__ import annotations


from datetime import date

from pydantic import BaseModel, ConfigDict





class DividendModel(BaseModel):
    """
    Модель дивидендов акции MOEX ISS.


    Используется:

    - DividendService
    - экспорт дивидендов
    - ClickHouse writer
    - дивидендная аналитика
    - уведомления


    Источник:

    MOEX ISS:

        /iss/securities/{SECID}/dividends.json


    Поля MOEX:

    - secid
    - isin
    - registryclosedate
    - value
    - currencyid

    """



    model_config = ConfigDict(
        extra="ignore"
    )



    # --------------------------------------------------
    # Идентификаторы акции
    # --------------------------------------------------

    secid: str = ""

    isin: str = ""



    # --------------------------------------------------
    # Дивидендные данные
    # --------------------------------------------------

    registry_close_date: date | None = None

    value: float = 0.0

    currency: str = ""



    # --------------------------------------------------
    # Дополнительная аналитика
    # --------------------------------------------------

    dividend_yield: float = 0.0


    payment_date: date | None = None


    comment: str = ""