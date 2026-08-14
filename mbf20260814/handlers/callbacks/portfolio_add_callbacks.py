from maxapi import Router
from maxapi.context.base import BaseContext
from maxapi.types import MessageCallback


from app.states.user import UserStates


from app.payloads.callback_payloads import (
    AddPortfolioPayload,
    AddPortfolioFromMenuPayload
)



print(
    "PORTFOLIO ADD CALLBACKS LOADED"
)



router = Router()



# ==================================================
# Добавление акции из меню ПОРТФЕЛЬ
# ==================================================

@router.message_callback(
    AddPortfolioFromMenuPayload.filter()
)
async def portfolio_add_from_menu_callback(

        event: MessageCallback,

        context: BaseContext

):


    print("=" * 50)
    print("PORTFOLIO ADD FROM MENU")
    print(
        "PAYLOAD:",
        event.callback.payload
    )
    print("=" * 50)



    await event.answer()



    # ВАЖНО:
    # отдельное состояние,
    # чтобы не запускался ticker_quotes_handler

    await context.set_state(

        UserStates.WAIT_PORTFOLIO_TICKER

    )



    print(
        "STATE:",
        await context.get_state()
    )



    await event.message.answer(

        "➕ Добавление акции\n\n"
        "Введите тикер:\n\n"
        "Например:\n"
        "GAZP"

    )



# ==================================================
# Добавление акции из КОТИРОВКИ
# ==================================================

@router.message_callback(
    AddPortfolioPayload.filter()
)
async def portfolio_add_from_quote_callback(

        event: MessageCallback,

        context: BaseContext

):


    print("=" * 50)
    print("PORTFOLIO ADD FROM QUOTE")
    print(
        "PAYLOAD:",
        event.callback.payload
    )
    print("=" * 50)



    await event.answer()



    data = await context.get_data()



    ticker = data.get(
        "ticker"
    )



    print(
        "CURRENT TICKER:",
        ticker
    )



    if not ticker:


        await event.message.answer(

            "❌ Сначала выберите акцию"

        )

        return



    # сохраняем тикер для портфеля

    await context.update_data(

        portfolio_ticker=ticker

    )



    # дальше сразу ввод количества

    await context.set_state(

        UserStates.WAIT_PORTFOLIO_QUANTITY

    )



    print(
        "STATE:",
        await context.get_state()
    )



    await event.message.answer(

        f"➕ Добавление {ticker}\n\n"
        "Введите количество акций:\n\n"
        "Например:\n"
        "10"

    )