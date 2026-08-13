from maxapi import Router, F
from maxapi.types import MessageCreated
from maxapi.context.base import BaseContext
from app.utils.portfolio_formatter import (PortfolioFormatter)

from app.states.user import UserStates
from app.keyboards.general_menu import main_menu

from app.services.portfolio_service import PortfolioService
from app.services.portfolio_history_service import PortfolioHistoryService



print(
    "PORTFOLIO SELL PRICE HANDLER LOADED"
)



router = Router()



portfolio_service = PortfolioService()

portfolio_history_service = PortfolioHistoryService()



# ==================================================
# ВВОД ЦЕНЫ ПРОДАЖИ
# ==================================================

@router.message_created(

    UserStates.WAIT_SELL_PRICE,

    F.message.body.text

)
async def portfolio_sell_price_handler(

        event: MessageCreated,

        context: BaseContext

):


    print("=" * 50)

    print(
        "PORTFOLIO SELL PRICE HANDLER"
    )

    print("=" * 50)



    if not event.message.body or not event.message.body.text:


        await event.message.answer(

            "❌ Введите цену продажи"

        )

        return



    price_text = (

        event.message.body.text

        .strip()

        .replace(",", ".")

    )



    try:

        sell_price = float(price_text)


    except ValueError:


        await event.message.answer(

            """
❌ Некорректная цена


Введите число:

Например:
263.50
"""

        )

        return



    if sell_price <= 0:


        await event.message.answer(

            "❌ Цена продажи должна быть больше 0"

        )

        return



    user_id = event.from_user.user_id



    data = await context.get_data()



    print(

        "SELL DATA:",

        data

    )



    ticker = data.get(

        "sell_ticker"

    )


    quantity = data.get(

        "sell_quantity"

    )


    buy_price = data.get(

        "sell_buy_price"

    )



    if (

        not ticker

        or quantity is None

        or buy_price is None

    ):


        await event.message.answer(

            "❌ Ошибка данных продажи. Начните заново."

        )


        await context.clear()


        return



    # ==============================
    # Расчет сделки
    # ==============================


    buy_total = (

        quantity *

        buy_price

    )


    sell_total = (

        quantity *

        sell_price

    )


    profit = (

        sell_total -

        buy_total

    )


    percent = (

        profit /

        buy_total *

        100

    ) if buy_total else 0



    print(

        "SELL RESULT",

        {

            "ticker": ticker,

            "quantity": quantity,

            "buy_price": buy_price,

            "sell_price": sell_price,

            "profit": profit

        }

    )

    # ==============================
    # Проверяем лимит истории
    # ==============================

    can_sell = await portfolio_history_service.can_add_history(

        user_id=user_id

    )

    if not can_sell:
        await event.message.answer(

            """
⚠️ Нельзя выполнить продажу


📜 История сделок заполнена:

10 / 10


Очистите историю сделок,
чтобы продолжить продажи.
"""

        )

        await context.clear()

        return

    # ==============================
    # Сохраняем историю продажи
    # ==============================

    history_result = await portfolio_history_service.add_sell_history(

        user_id=user_id,

        ticker=ticker,

        quantity=quantity,

        buy_price=buy_price,

        sell_price=sell_price

    )

    if history_result is None:
        await event.message.answer(

            "❌ Не удалось сохранить историю сделки"

        )

        await context.clear()

        return

    print(

        "SELL HISTORY SAVED"

    )

    # ==============================
    # Уменьшаем позицию
    # ==============================

    sell_result = await portfolio_service.sell_position(

        user_id=user_id,

        ticker=ticker,

        quantity=quantity

    )

    print(

        "SELL POSITION RESULT:",

        sell_result

    )

    if not sell_result:
        await event.message.answer(

            "❌ Не удалось изменить портфель"

        )

        return

    # ==============================
    # Ответ пользователю
    # ==============================

    await event.message.answer(

        f"""
✅ Акция продана


📈 {ticker}


Количество:
{quantity:.2f} шт.


💰 Покупка:
{buy_total:.2f} ₽


💵 Продажа:
{sell_total:.2f} ₽


Результат:
{profit:+.2f} ₽


Доходность:
{percent:+.2f}%


📂 История сделки сохранена

"""

    )

    # =====================================
    # Получаем обновленный портфель
    # =====================================

    portfolio = await portfolio_service.get_portfolio(

        user_id=user_id

    )

    portfolio_message = await PortfolioFormatter.format_portfolio(

        portfolio,

        user_id

    )

    await context.clear()

    print(
        "SELL CONTEXT CLEARED"
    )

    # =====================================
    # Отправляем обновленный портфель
    # =====================================

    await event.message.answer(

        portfolio_message

    )

    # =====================================
    # Главное меню
    # =====================================

    await event.message.answer(

        "Выберите действие:",

        attachments=[

            main_menu()

        ]

    )