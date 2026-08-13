from maxapi import Router

from maxapi.types import MessageCallback
from maxapi.context.base import BaseContext


from app.payloads.callback_payloads import (
    HistoryPayload
)


from app.services.ticker_history_service import (
    TickerHistoryService
)


from app.utils.ticker_history_formatter import (
    format_history
)


from app.keyboards.ticker_general_menu import (
    quote_menu
)



print(
    "TICKER HISTORY CALLBACK LOADED"
)



router = Router()


service = TickerHistoryService()



# ==================================================
# ИСТОРИЯ ТИКЕРА
# ==================================================

@router.message_callback(

    HistoryPayload.filter()

)
async def ticker_history_callback(

        event: MessageCallback,

        context: BaseContext

):


    print("=" * 50)

    print(
        "HISTORY CALLBACK"
    )

    print(
        "PAYLOAD:",
        event.callback.payload
    )

    print("=" * 50)



    await event.answer()



    # ==================================================
    # Получаем выбранный тикер
    # ==================================================

    data = await context.get_data()


    print(
        "CONTEXT:",
        data
    )



    ticker = data.get(

        "ticker"

    )



    if not ticker:


        await event.message.answer(

            "❌ Тикер не найден"

        )

        return



    print(

        "HISTORY TICKER:",

        ticker

    )



    # ==================================================
    # Получаем историю
    # ==================================================

    history = await service.get_history(

        ticker=ticker,

        limit=7

    )



    print(

        "HISTORY DATA:",

        history

    )



    if not history:


        await event.message.answer(

            f"❌ Нет истории по {ticker}"

        )

        return



    # ==================================================
    # Форматирование
    # ==================================================

    text = format_history(

        ticker,

        history

    )



    # ==================================================
    # Ответ + меню
    # ==================================================

    await event.message.answer(

        text,

        attachments=[

            quote_menu()

        ]

    )



    print(

        "HISTORY SENT"

    )