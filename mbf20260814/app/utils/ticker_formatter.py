from app.utils.date_utils import format_date_ru


def formatter_quote(quote: dict):
    formatted_date = format_date_ru(quote['date'])

    return (
        f"📊 {quote['name']}\n\n"

        f"🏷 Тикер: {quote['ticker']}\n\n"

        f"💰 Цена: {quote['price']} ₽\n\n"

        f"📅 Дата: {formatted_date}\n\n"

        f"🏭 Сектор: {quote['sector']}"
    )