from maxapi import Router
from maxapi.types import MessageCallback
from maxapi.context.base import BaseContext


from app.services.portfolio_service import PortfolioService
from app.utils.portfolio_formatter import (
    PortfolioFormatter
)


from app.keyboards.portfolio_general_menu import portfolio_menu


from app.payloads.callback_payloads import PortfolioPayload



print(
    "PORTFOLIO CALLBACK LOADED"
)



router = Router()


portfolio_service = PortfolioService()



@router.message_callback(
    PortfolioPayload.filter()
)
async def portfolio_callback(

        event: MessageCallback,

        context: BaseContext

):


    print("=" * 50)

    print(
        "PORTFOLIO CALLBACK"
    )

    print(
        "PAYLOAD:",
        event.callback.payload
    )

    print("=" * 50)



    await event.answer()



    user_id = event.from_user.user_id



    print(
        "USER ID:",
        user_id
    )



    portfolio = await portfolio_service.get_portfolio(

        user_id=user_id

    )



    print(
        "PORTFOLIO RESULT:",
        portfolio
    )



    if not portfolio:


        await event.message.answer(

            "📊 Мой портфель пуст\n\n"
            "Добавьте акции через меню котировки.",

            attachments=[

                portfolio_menu()

            ]

        )


        return



    # =====================================
    # Форматирование портфеля
    # =====================================

    text = await PortfolioFormatter.format_portfolio(

        portfolio,

        user_id

    )



    await event.message.answer(

        text,

        attachments=[

            portfolio_menu()

        ]

    )



    print(
        "PORTFOLIO MESSAGE SENT"
    )