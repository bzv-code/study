from maxapi import Router, F

from maxapi.types import MessageCreated
from maxapi.context.base import BaseContext

from app.states.user import UserStates
from app.services.ticker_service import TickerService
from app.keyboards.alert_condition_menu import (
    alert_condition_menu
)


print(
    "ALERT QUOTES LOADED"
)


router = Router()

ticker_service = TickerService()


# ==================================================
# ВВОД ТИКЕРА
# ==================================================

@router.message_created(
    UserStates.WAIT_ALERT_TICKER,
    F.message.body.text
)
async def alert_ticker_handler(
        event: MessageCreated,
        context: BaseContext
):

    text = event.message.body.text.strip()

    ticker = text.upper()

    print(
        "ALERT TICKER:",
        ticker
    )

    quote = await ticker_service.get_quote(
        ticker
    )

    if not quote:

        await event.message.answer(
            f"❌ Акция {ticker} не найдена"
        )

        return

    await context.update_data(

        alert_ticker=ticker

    )

    await context.set_state(

        UserStates.WAIT_ALERT_PRICE

    )

    print(
        "STATE -> WAIT_ALERT_PRICE"
    )

    await event.message.answer(

        f"🔔 {ticker}\n\n"
        "Введите цену уведомления:"

    )


# ==================================================
# ВВОД ЦЕНЫ
# ==================================================

@router.message_created(
    UserStates.WAIT_ALERT_PRICE,
    F.message.body.text
)
async def alert_price_handler(
        event: MessageCreated,
        context: BaseContext
):

    text = event.message.body.text.strip()

    try:

        price = float(

            text.replace(",", ".")

        )

    except ValueError:

        await event.message.answer(

            "❌ Введите цену числом\n\n"
            "Например:\n"
            "100"

        )

        return

    data = await context.get_data()

    ticker = data.get(
        "alert_ticker"
    )

    if ticker is None:

        await context.clear()

        await event.message.answer(

            "❌ Тикер не найден.\n"
            "Попробуйте создать уведомление заново."

        )

        return

    await context.update_data(

        alert_price=price

    )

    await context.set_state(

        UserStates.WAIT_ALERT_CONDITION

    )

    print(
        "STATE -> WAIT_ALERT_CONDITION"
    )

    await event.message.answer(

        f"🔔 {ticker}\n\n"
        f"Цена уведомления: {price:.2f} ₽\n\n"
        "Выберите условие:",

        attachments=[

            alert_condition_menu()

        ]

    )