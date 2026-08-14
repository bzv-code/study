from maxapi import Router, F

from maxapi.types import MessageCreated
from maxapi.context.base import BaseContext


from app.states.user import UserStates


from app.services.ticker_service import TickerService


from app.keyboards.analysis_ticker_period_menu import (
    analysis_ticker_period_menu
)



print(
    "ANALYSIS QUOTES LOADED"
)



router = Router()



ticker_service = TickerService()



# ==================================================
# ВВОД ТИКЕРА ДЛЯ АНАЛИЗА
# ==================================================

@router.message_created(

    UserStates.WAIT_ANALYSIS_TICKER,

    F.message.body.text

)

async def analysis_quotes_handler(

        event: MessageCreated,

        context: BaseContext

):


    print("=" * 50)

    print(
        "ANALYSIS HANDLER EVENT"
    )

    print("=" * 50)



    if not event.message.body or not event.message.body.text:


        await event.message.answer(

            "❌ Введите тикер акции"

        )

        return



    ticker = (

        event.message.body.text

        .strip()

        .upper()

    )



    print(
        "ANALYSIS TICKER:",
        ticker
    )



    if not ticker:


        await event.message.answer(

            "❌ Введите тикер акции"

        )

        return



    # =====================================
    # Проверяем существование акции
    # =====================================

    quote = await ticker_service.get_quote(

        ticker

    )


    print(
        "QUOTE:",
        quote
    )



    if not quote:


        await event.message.answer(

            f"❌ Не удалось найти акцию {ticker}\n\n"

            "Введите корректный тикер."

        )

        return



    # =====================================
    # Сохраняем тикер
    # =====================================

    await context.update_data(

        analysis_ticker=ticker

    )



    print(

        "ANALYSIS TICKER SAVED:",

        ticker

    )



    # =====================================
    # Переходим к выбору периода
    # =====================================

    await context.set_state(

        UserStates.WAIT_ANALYSIS_PERIOD

    )



    print(

        "STATE -> WAIT_ANALYSIS_PERIOD"

    )



    # =====================================
    # Выводим меню периодов
    # =====================================

    await event.message.answer(

        f"""
📉 Анализ {ticker}


Выберите период:
""",

        attachments=[

            analysis_ticker_period_menu()

        ]

    )



    print(
        "WAITING ANALYSIS PERIOD"
    )

    print("=" * 50)