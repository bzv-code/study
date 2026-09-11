"""Бизнес-логика заказов: создание заказа из корзины, пересчёт суммы, смена статуса + уведомление бота."""


async def create_order_from_cart(user_id: int, items: list, address: str, delivery_time: str) -> dict:
    # TODO: посчитать сумму по позициям, сохранить заказ в БД, вернуть данные для оплаты
    raise NotImplementedError


async def update_order_status(order_id: int, status: str) -> None:
    # TODO: обновить статус в БД и дёрнуть бота (webhook/очередь), чтобы уведомить пользователя
    raise NotImplementedError
