def formatter_quote(
        quote: dict
):

    return (
        f"📊 {quote['name']}\n\n"

        f"🏷 Тикер: {quote['ticker']}\n\n"

        f"💰 Цена: {quote['price']} ₽\n\n"

        f"📅 Дата: {quote['date']}\n\n"

        f"🏭 Сектор: {quote['sector']}"
    )