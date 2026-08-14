from datetime import datetime


def format_date_ru(date_value) -> str:
    """
    Конвертирует дату из различных форматов в русский формат DD.MM.YYYY

    Args:
        date_value: Объект datetime, строка или другой формат даты

    Returns:
        Строка в формате '31.07.2026'
    """

    # Если уже строка, пробуем распарсить
    if isinstance(date_value, str):
        # Пробуем разные форматы
        formats = [
            "%Y-%m-%d",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%dT%H:%M:%S.%f",
            "%Y-%m-%d %H:%M:%S%z",
        ]

        for fmt in formats:
            try:
                dt = datetime.strptime(date_value.split('+')[0].split('.')[0], fmt.replace('%z', ''))
                return dt.strftime("%d.%m.%Y")
            except ValueError:
                continue

        # Если не удалось распарсить, возвращаем как есть
        return date_value

    # Если объект datetime
    if isinstance(date_value, datetime):
        return date_value.strftime("%d.%m.%Y")

    # Если другой тип, конвертируем в строку
    return str(date_value)