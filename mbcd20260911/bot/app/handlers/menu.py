"""Обработка нажатий на callback-кнопки главного меню.

message_callback() в maxapi 0.9.4 не принимает фильтр — разбор по payload
делаем вручную внутри одного хендлера.
"""
from maxapi import Router
from maxapi.types import MessageCallback

router = Router()


@router.message_callback()
async def callback_handler(event: MessageCallback) -> None:
    payload = event.callback.payload

    if payload == "orders":
        # TODO: запросить список заказов пользователя у backend по chat_id/max_user_id
        await event.message.answer("Здесь появится список ваших заказов.")
    elif payload == "support":
        await event.message.answer(
            "Частые вопросы:\n"
            "• сроки доставки\n"
            "• зоны доставки\n"
            "• отмена заказа\n\n"
            "Если не нашли ответ — напишите нам."
        )
    elif payload == "profile":
        # TODO: запросить профиль пользователя у backend
        await event.message.answer("Здесь будут ваши адреса, телефон и бонусы.")
