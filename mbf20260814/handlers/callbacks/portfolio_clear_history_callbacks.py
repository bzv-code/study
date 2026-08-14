from maxapi import Router

from maxapi.types import MessageCallback

from maxapi.context.base import BaseContext


from app.payloads.callback_payloads import (
    ClearHistoryPayload
)


from app.services.portfolio_history_service import (
    PortfolioHistoryService
)


from app.keyboards.portfolio_general_menu import (
    portfolio_menu
)



print(
    "PORTFOLIO CLEAR HISTORY CALLBACK LOADED"
)



router = Router()



history_service = PortfolioHistoryService()



@router.message_callback(

    ClearHistoryPayload.filter()

)

async def portfolio_clear_history_callback(

        event: MessageCallback,

        context: BaseContext

):


    await event.answer()



    user_id = event.from_user.user_id



    result = await history_service.clear_history(

        user_id=user_id

    )



    # =====================================
    # Получаем обновленную статистику
    # =====================================

    statistics = await history_service.get_statistics(

        user_id=user_id

    )



    if result:


        prefix = (

            "🗑 История сделок очищена\n\n"

        )


    else:


        prefix = (

            "📜 История сделок уже была пустая\n\n"

        )



    text = (

        prefix

        +

        "📜 История сделок\n\n"

        f"Сделок: {statistics['trades']} / 10\n\n"

        f"✅ Прибыльных: {statistics['win_trades']}\n"

        f"❌ Убыточных: {statistics['loss_trades']}\n\n"

        f"💰 Прибыль: {statistics['total']:+.2f} ₽"

    )



    await event.message.answer(

        text,

        attachments=[

            portfolio_menu()

        ]

    )