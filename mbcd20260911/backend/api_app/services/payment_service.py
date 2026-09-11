"""Интеграция с платёжным провайдером: создание платежа, проверка вебхука."""


async def create_payment(order_id: int, amount: int) -> dict:
    # TODO: вызвать API провайдера (ЮKassa/CloudPayments), вернуть ссылку/токен оплаты
    raise NotImplementedError


async def handle_webhook(payload: dict) -> None:
    # TODO: проверить подпись вебхука, обновить статус оплаты заказа
    raise NotImplementedError
