from maxapi import Router
from maxapi.context.base import BaseContext
from maxapi.types import MessageCallback


from app.states.user import UserStates


from app.payloads.callback_payloads import (
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
# УДАЛЕНО: Добавление акции из КОТИРОВКИ
# ==================================================

# @router.message_callback(
#     AddPortfolioPayload.filter()
# )
# async def portfolio_add_from_quote_callback(
#
#         event: MessageCallback,
#
#         context: BaseContext
#
# ):
#     ... (код удалён, т.к. убрана кнопка Котировки)