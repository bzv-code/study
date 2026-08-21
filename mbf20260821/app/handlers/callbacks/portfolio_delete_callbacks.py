from maxapi import Router
from maxapi.types import MessageCallback
from maxapi.context.base import BaseContext

from app.states.user import UserStates
from app.services.portfolio_service import PortfolioService
from app.payloads.callback_payloads import DeletePortfolioPayload


print(
    "DELETE PORTFOLIO CALLBACK LOADED"
)


router = Router()

portfolio_service = PortfolioService()


@router.message_callback(
    DeletePortfolioPayload.filter()
)
async def delete_portfolio_callback(
        event: MessageCallback,
        context: BaseContext
):

    print("=" * 50)
    print("DELETE PORTFOLIO CALLBACK")
    print("=" * 50)


    await event.answer()


    # =====================================
    # Получаем пользователя
    # =====================================

    user_id = None


    if hasattr(event, "from_user"):

        user_id = event.from_user.user_id


    elif hasattr(event.message, "user_id"):

        user_id = event.message.user_id


    elif hasattr(event.message, "user"):

        user_id = event.message.user.user_id



    print(
        "DELETE USER ID:",
        user_id
    )


    if not user_id:

        await event.message.answer(
            "❌ Не удалось определить пользователя"
        )

        return



    # =====================================
    # Получаем текущий портфель
    # =====================================

    portfolio = await portfolio_service.get_portfolio(
        user_id=user_id
    )


    print(
        "CURRENT PORTFOLIO:",
        portfolio
    )



    if not portfolio:

        await event.message.answer(
            "📂 Ваш портфель пуст"
        )

        await context.clear()

        return



    tickers = []


    for item in portfolio:

        tickers.append(
            item["ticker"]
        )



    message = (

        "❌ Удаление акции\n\n"

        "Введите тикер:\n\n"

        "Ваш портфель:\n"

        + "\n".join(
            [
                f"📈 {ticker}"
                for ticker in tickers
            ]
        )

        +

        "\n\nНапример:\nGAZP"

    )



    await event.message.answer(
        message
    )



    await context.set_state(
        UserStates.WAIT_DELETE_TICKER
    )