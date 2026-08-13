from maxapi import Router

from maxapi.types import MessageCallback
from maxapi.context.base import BaseContext


from app.payloads.callback_payloads import (
    HistoryPayload
)


from app.services.portfolio_history_service import (
    PortfolioHistoryService
)


from app.keyboards.portfolio_general_menu import (
    portfolio_menu
)



print(
    "PORTFOLIO HISTORY CALLBACK LOADED"
)



router = Router()



history_service = PortfolioHistoryService()



# ==================================================
# ИСТОРИЯ СДЕЛОК ПОРТФЕЛЯ
# ==================================================

@router.message_callback(

    HistoryPayload.filter()

)

async def portfolio_history_callback(

        event: MessageCallback,

        context: BaseContext

):


    print("=" * 50)

    print(
        "PORTFOLIO HISTORY CALLBACK"
    )

    print(
        "PAYLOAD:",
        event.callback.payload
    )

    print("=" * 50)



    await event.answer()



    user_id = event.from_user.user_id



    # ==================================================
    # Получаем историю сделок
    # ==================================================

    history = await history_service.get_history(

        user_id=user_id

    )



    # ==================================================
    # Получаем статистику
    # ==================================================

    statistics = await history_service.get_statistics(

        user_id=user_id

    )



    if not history:


        text = (

            "📜 История сделок пустая\n\n"

            "Продайте акции, чтобы здесь появились сделки."

        )


        await event.message.answer(

            text,

            attachments=[

                portfolio_menu()

            ]

        )


        return



    # ==================================================
    # Формируем ответ
    # ==================================================

    text = (

        "📜 История сделок\n\n"

        f"📊 Всего сделок: {statistics['trades']} / 10\n\n"

        f"✅ Прибыльных: {statistics['win_trades']}\n"

        f"❌ Убыточных: {statistics['loss_trades']}\n\n"

        f"💰 Общий результат: {statistics['total']:+.2f} ₽\n\n"

        "━━━━━━━━━━━━━━\n\n"

    )



    # ==================================================
    # Список сделок
    # ==================================================

    for index, item in enumerate(

            history,

            start=1

    ):


        emoji = (

            "✅"

            if item.profit >= 0

            else

            "❌"

        )



        text += (

            f"{index}. {emoji} {item.ticker}\n\n"

            f"📦 Количество: "

            f"{item.quantity:.2f} шт.\n"

            f"💰 Покупка: "

            f"{item.buy_price:.2f} ₽\n"

            f"💵 Продажа: "

            f"{item.sell_price:.2f} ₽\n"

            f"📈 Результат: "

            f"{item.profit:+.2f} ₽\n"

            f"📅 Дата: "

            f"{item.sell_date}\n\n"

        )



    # ==================================================
    # Отправка сообщения
    # ==================================================

    await event.message.answer(

        text,

        attachments=[

            portfolio_menu()

        ]

    )


    print(
        "PORTFOLIO HISTORY SENT"
    )