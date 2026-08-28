from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo


# Часовой пояс Московской биржи
MOSCOW_TZ = ZoneInfo("Europe/Moscow")


def parse_moscow_datetime(
    value: str | datetime,
) -> datetime:
    """
    Преобразовать дату/время MOEX
    в datetime с часовым поясом Europe/Moscow.

    Поддерживает:

    2026-07-31
    2026-07-31 10:15:00
    2026-07-31T10:15:00
    datetime(...)
    """

    if isinstance(value, datetime):

        if value.tzinfo is None:

            return value.replace(
                tzinfo=MOSCOW_TZ
            )

        return value.astimezone(
            MOSCOW_TZ
        )

    value = value.strip()

    # ISO формат
    value = value.replace(
        "T",
        " ",
    )

    # только дата
    if len(value) == 10:

        dt = datetime.strptime(
            value,
            "%Y-%m-%d",
        )

    else:

        dt = datetime.strptime(
            value,
            "%Y-%m-%d %H:%M:%S",
        )

    return dt.replace(
        tzinfo=MOSCOW_TZ
    )


def now_moscow() -> datetime:
    """
    Текущее московское время.
    """

    return datetime.now(
        MOSCOW_TZ
    )


def format_moscow(
    value: datetime,
) -> str:
    """
    datetime -> строка
    YYYY-MM-DD HH:MM:SS
    """

    return value.astimezone(
        MOSCOW_TZ
    ).strftime(
        "%Y-%m-%d %H:%M:%S"
    )


def date_only(
    value: str | datetime,
) -> str:
    """
    Получить дату
    YYYY-MM-DD.
    """

    return parse_moscow_datetime(
        value
    ).strftime(
        "%Y-%m-%d"
    )


def datetime_only(
    value: str | datetime,
) -> datetime:
    """
    Алиас для parse_moscow_datetime().
    Удобно использовать в writer'ах.
    """

    return parse_moscow_datetime(
        value
    )