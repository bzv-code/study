from maxapi import Router

from maxapi.types import MessageCallback
from maxapi.context.base import BaseContext


from app.states.user import UserStates


from app.payloads.callback_payloads import (
    CreateAlertFromQuotePayload
)



print(
    "ALERT TICKER CALLBACK LOADED"
)



router = Router()



# ==================================================
# СОЗДАНИЕ УВЕДОМЛЕНИЯ ИЗ МЕНЮ КОТИРОВКИ
# ==================================================

@router.message_callback(
    CreateAlertFromQuotePayload.filter()
)
async def alert_ticker_callback(
        event: MessageCallback,
        context: BaseContext
):


    print("=" * 50)

    print(
        "ALERT FROM TICKER CALLBACK"
    )

    print(
        "PAYLOAD:",
        event.callback.payload
    )

    print("=" * 50)



    await event.answer()



    # Получаем текущий тикер

    data = await context.get_data()



    print(
        "QUOTE CONTEXT:",
        data
    )



    ticker = data.get(
        "ticker"
    )



    if not ticker:


        await event.message.answer(

            "❌ Не найден выбранный тикер"

        )


        await context.clear()

        return



    ticker = ticker.upper().strip()



    # ==================================================
    # СОХРАНЯЕМ ДАННЫЕ ДЛЯ СОЗДАНИЯ УВЕДОМЛЕНИЯ
    # ==================================================

    await context.update_data(

        ticker=ticker,

        alert_ticker=ticker,

        alert_price=None,

        alert_source="quote"

    )



    await context.set_state(

        UserStates.WAIT_ALERT_PRICE

    )



    await event.message.answer(

        f"""
🔔 {ticker}


Введите цену уведомления:
"""

    )



    print(

        "ALERT TICKER:",

        ticker

    )


    print(

        "STATE -> WAIT_ALERT_PRICE"

    )