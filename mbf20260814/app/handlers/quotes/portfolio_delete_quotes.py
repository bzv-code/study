from maxapi import Router, F
from maxapi.types import MessageCreated
from maxapi.context.base import BaseContext

from app.states.user import UserStates

from app.services.portfolio_service import PortfolioService

from app.keyboards.portfolio_general_menu import portfolio_menu


print(
    "PORTFOLIO DELETE QUOTES LOADED"
)


router = Router()


portfolio_service = PortfolioService()



@router.message_created(
    UserStates.WAIT_DELETE_TICKER,
    F.message.body.text
)
async def portfolio_delete_quotes_handler(

        event: MessageCreated,

        context: BaseContext

):


    print("=" * 50)
    print("PORTFOLIO DELETE HANDLER")
    print("=" * 50)



    ticker = (

        event.message.body.text

        .strip()

        .upper()

    )


    user_id = event.from_user.user_id



    print(
        "DELETE:",
        user_id,
        ticker
    )



    deleted = await portfolio_service.delete_by_ticker(

        user_id=user_id,

        ticker=ticker

    )



    print(
        "DELETE RESULT:",
        deleted
    )



    if not deleted:


        await event.message.answer(

            f"""
❌ В портфеле нет акции

📈 {ticker}
"""

        )


        await context.clear()

        return




    await event.message.answer(

        f"""
✅ Все покупки удалены

📈 {ticker}
"""

    )



    portfolio = await portfolio_service.get_portfolio(

        user_id=user_id

    )



    if not portfolio:


        await event.message.answer(

            "📊 Портфель пуст",

            attachments=[

                portfolio_menu()

            ]

        )


        await context.clear()

        return




    message = "📊 Мой портфель\n\n"



    total_invested = 0

    total_value = 0



    for item in portfolio:


        total_invested += item["invested"]

        total_value += item["current_value"]



        emoji = "📈" if item["profit"] >= 0 else "📉"



        message += (

            f"{emoji} {item['ticker']}\n"

            f"Количество: {item['quantity']:.2f}\n"

            f"Средняя цена: {item['buy_price']:.2f} ₽\n"

            f"Текущая цена: {item['current_price']:.2f} ₽\n"

            f"Результат: {item['profit']:+.2f} ₽\n"

            f"Доходность: {item['percent']:+.2f}%\n"

            "\n----------------\n\n"

        )




    profit = total_value - total_invested


    percent = (

        profit / total_invested * 100

    ) if total_invested else 0




    message += (

        "📌 ИТОГО\n\n"

        f"💰 Вложено: {total_invested:.2f} ₽\n"

        f"📦 Стоимость: {total_value:.2f} ₽\n"

        f"Результат: {profit:+.2f} ₽\n"

        f"Доходность: {percent:+.2f}%"

    )



    await event.message.answer(

        message,

        attachments=[

            portfolio_menu()

        ]

    )



    await context.clear()



    print(
        "DELETE FINISHED"
    )