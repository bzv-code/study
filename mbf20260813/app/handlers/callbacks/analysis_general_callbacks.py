from maxapi import Router

from maxapi.types import MessageCallback
from maxapi.context.base import BaseContext


from app.payloads.callback_payloads import (
    AnalysisPayload
)


from app.keyboards.analysis_general_menu import (
    analysis_general_menu
)


from app.services.analysis_stocks_service import (
    AnalysisStocksService
)


print(
    "ANALYSIS GENERAL CALLBACK LOADED"
)


router = Router()


analysis_service = AnalysisStocksService()



# ==================================================
# ФОРМАТИРОВАНИЕ АНАЛИЗА
# ==================================================

def format_market_top(result):

    text = (
        "📊 Анализ рынка\n\n"
        "📈 ТОП 5 роста за 7 дней:\n\n"
    )


    growth = result.get(
        "stocks_growth",
        []
    )


    for index, stock in enumerate(
            growth,
            start=1
    ):

        text += (

            f"{index}. "
            f"{stock['ticker']} "
            f"+{stock['change_percent']:.2f}%\n"

        )


    text += "\n📉 ТОП 5 падения за 7 дней:\n\n"


    fall = result.get(
        "stocks_fall",
        []
    )


    for index, stock in enumerate(
            fall,
            start=1
    ):

        text += (

            f"{index}. "
            f"{stock['ticker']} "
            f"{stock['change_percent']:.2f}%\n"

        )


    return text



# ==================================================
# КНОПКА АНАЛИЗ
# ==================================================

@router.message_callback(

    AnalysisPayload.filter()

)

async def analysis_general_callback(

        event: MessageCallback,

        context: BaseContext

):


    print("=" * 50)

    print(
        "ANALYSIS GENERAL CALLBACK"
    )

    print(
        "PAYLOAD:",
        event.callback.payload
    )

    print("=" * 50)



    await event.answer()


    await context.clear()



    try:


        result = await analysis_service.analyze_stocks(

            period=7

        )


        text = format_market_top(

            result

        )


    except Exception as e:


        print(
            "ANALYSIS TOP ERROR:",
            e
        )


        text = (

            "📊 Анализ рынка\n\n"

            "❌ Не удалось получить данные."

        )



    await event.message.answer(

        text,

        attachments=[

            analysis_general_menu()

        ]

    )