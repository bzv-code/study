"""Отправка уведомлений пользователю о смене статуса заказа (принят, собран, курьер выехал, доставлен).

Вызывается из backend после смены статуса заказа (например, HTTP-запросом к
небольшому внутреннему эндпоинту бота). chat_id для личной переписки с ботом
в MAX совпадает с chat_id, полученным в событии BotStarted/MessageCreated —
его нужно сохранить в таблице users при первом обращении пользователя.
"""
from maxapi import Bot

STATUS_TEXT = {
    "accepted": "Заказ принят в работу",
    "assembled": "Букет собран",
    "on_the_way": "Курьер выехал к вам",
    "delivered": "Заказ доставлен",
}


async def notify_order_status(bot: Bot, chat_id: int, order_id: str, status: str) -> None:
    text = STATUS_TEXT.get(status, status)
    await bot.send_message(chat_id=chat_id, text=f"Заказ {order_id}: {text}")
