from maxapi import Router
from maxapi.types import MessageCallback
from maxapi.context.base import BaseContext


from app.services.portfolio_service import PortfolioService

from app.payloads.callback_payloads import (
    SellPortfolioPayload
)

from app.keyboards.sell_mode_menu import (
    sell_mode_menu
)



print(
    "SELL PORTFOLIO CALLBACK LOADED"
)



router = Router()



portfolio_service = PortfolioService()




@router.message_callback(
    SellPortfolioPayload.filter()
)
async def sell_portfolio_callback(

        event: MessageCallback,

        context: BaseContext

):


    print("=" * 50)

    print(
        "SELL PORTFOLIO CALLBACK"
    )

    print("=" * 50)



    await event.answer()



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
    # Выбор способа продажи
    # =====================================

    await event.message.answer(

        "Как вы хотите продать акцию?",

        attachments=[

            sell_mode_menu()

        ]

    )