from maxapi import Router, F
from maxapi.types import MessageCreated
from maxapi.context.base import BaseContext

from app.states.user import UserStates
from app.services.portfolio_service import PortfolioService
from app.keyboards.portfolio_general_menu import portfolio_menu


print("PORTFOLIO ADD QUOTES LOADED")


router = Router()


portfolio_service = PortfolioService()



async def process_portfolio_add(
    event: MessageCreated,
    context: BaseContext
):

    print("=" * 50)
    print("PORTFOLIO ADD HANDLER")
    print("=" * 50)


    state = await context.get_state()


    print(
        "STATE:",
        state
    )


    if not event.message.body or not event.message.body.text:
        return


    text = event.message.body.text.strip()


    print(
        "INPUT:",
        text
    )


    # ==================================================
    # ШАГ 1. Количество акций
    # ==================================================

    if state == UserStates.WAIT_PORTFOLIO_QUANTITY:


        try:

            quantity = float(text)

        except ValueError:


            await event.message.answer(
                "❌ Введите количество числом\n\n"
                "Например: 10"
            )

            return



        await context.update_data(
            quantity=quantity
        )


        await context.set_state(
            UserStates.WAIT_PORTFOLIO_PRICE
        )


        print(
            "QUANTITY SAVED:",
            quantity
        )


        print(
            "STATE ->",
            await context.get_state()
        )


        await event.message.answer(
            "💰 Введите цену покупки:\n\n"
            "Например: 250.50"
        )


        return



    # ==================================================
    # ШАГ 2. Цена покупки
    # ==================================================

    if state == UserStates.WAIT_PORTFOLIO_PRICE:


        try:

            buy_price = float(text)

        except ValueError:


            await event.message.answer(
                "❌ Введите цену числом\n\n"
                "Например: 250.50"
            )

            return



        data = await context.get_data()


        ticker = data.get(
            "portfolio_ticker"
        )


        quantity = data.get(
            "quantity"
        )


        print(
            "PORTFOLIO DATA:",
            data
        )



        if not ticker:


            await event.message.answer(
                "❌ Не найден тикер"
            )

            await context.clear()

            return



        if quantity is None:


            await event.message.answer(
                "❌ Не найдено количество"
            )

            await context.clear()

            return



        user_id = event.from_user.user_id


        print(
            "SAVE POSITION:",
            ticker,
            quantity,
            buy_price
        )


        await portfolio_service.add_position(

            user_id=user_id,

            ticker=ticker,

            quantity=quantity,

            buy_price=buy_price

        )



        total = quantity * buy_price



        await event.message.answer(

            f"""
✅ Акция добавлена в портфель


📈 {ticker}

Количество:
{quantity:.2f} шт.

💰 Цена покупки:
{buy_price:.2f} ₽

💵 Инвестировано:
{total:.2f} ₽
"""

        )



        # Получаем обновленный портфель

        portfolio = await portfolio_service.get_portfolio(
            user_id=user_id
        )



        if portfolio:


            message = "📊 Мой портфель\n\n"


            total_invested = 0
            total_value = 0



            for item in portfolio:


                total_invested += item["invested"]

                total_value += item["current_value"]


                emoji = (
                    "📈"
                    if item["profit"] >= 0
                    else
                    "📉"
                )


                message += (

                    f"{emoji} {item['ticker']}\n"

                    f"Количество: {item['quantity']:.2f} шт.\n"

                    f"Средняя цена: {item['buy_price']:.2f} ₽\n"

                    f"Текущая цена: {item['current_price']:.2f} ₽\n"

                    f"Результат: {item['profit']:+.2f} ₽\n"

                    f"Доходность: {item['percent']:+.2f}%\n"

                    "----------------\n\n"

                )



            profit = total_value - total_invested


            percent = (

                profit / total_invested * 100

                if total_invested

                else 0

            )



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
            "PORTFOLIO ADD FINISHED"
        )



# ==================================================
# РЕГИСТРАЦИЯ ОБРАБОТЧИКОВ
# ==================================================


@router.message_created(
    UserStates.WAIT_PORTFOLIO_QUANTITY,
    F.message.body.text
)
async def portfolio_add_quantity_handler(
    event: MessageCreated,
    context: BaseContext
):

    await process_portfolio_add(
        event,
        context
    )



@router.message_created(
    UserStates.WAIT_PORTFOLIO_PRICE,
    F.message.body.text
)
async def portfolio_add_price_handler(
    event: MessageCreated,
    context: BaseContext
):

    await process_portfolio_add(
        event,
        context
    )