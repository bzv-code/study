from maxapi import Router
from maxapi.types import MessageCallback
from maxapi.context.base import BaseContext


from app.states.user import UserStates

from app.services.portfolio_service import PortfolioService

from app.payloads.callback_payloads import (
    SellModePayload
)



print(
    "SELL MODE CALLBACK LOADED"
)



router = Router()



portfolio_service = PortfolioService()



@router.message_callback(
    SellModePayload.filter()
)
async def sell_mode_callback(

        event: MessageCallback,

        context: BaseContext

):


    print("=" * 50)

    print(
        "SELL MODE CALLBACK"
    )

    print("=" * 50)



    await event.answer()



    # =====================================
    # Получаем режим: market / limit
    # =====================================

    payload = event.callback.payload


    mode = "market"


    if "|" in payload:


        _, mode_value = payload.split(

            "|",

            1

        )


        mode = mode_value



    print(
        "SELL MODE:",
        mode
    )



    user_id = event.from_user.user_id



    portfolio = await portfolio_service.get_portfolio(

        user_id=user_id

    )



    if not portfolio:


        await event.message.answer(

            "❌ Портфель пуст"

        )


        return



    # =====================================
    # Сохраняем режим продажи
    # =====================================

    await context.update_data(

        sell_mode=mode

    )



    # =====================================
    # Список портфеля + ввод тикера
    # =====================================

    message = (

        "📉 Продажа акции\n\n"

        "Ваш портфель:\n\n"

    )



    for item in portfolio:


        message += (

            f"📈 {item['ticker']}\n"

            f"Количество: {item['quantity']:.2f} шт.\n"

            f"Средняя цена: {item['buy_price']:.2f} ₽\n\n"

            "----------------\n\n"

        )



    message += (

        "Введите тикер акции:\n\n"

        "Например:\n"

        "GAZP"

    )



    await context.set_state(

        UserStates.WAIT_SELL_TICKER

    )



    print(

        "STATE ->",

        await context.get_state()

    )



    await event.message.answer(

        message

    )