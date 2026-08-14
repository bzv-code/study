from maxapi import Router

from maxapi.types import MessageCallback
from maxapi.context.base import BaseContext


from app.payloads.callback_payloads import (
    HomePayload
)


print(
    "HOME CALLBACK LOADED"
)


router = Router()



@router.message_callback(
    HomePayload.filter()
)
async def home_callback(
        event: MessageCallback,
        context: BaseContext
):


    print("=" * 50)
    print("HOME CALLBACK")
    print(
        "PAYLOAD:",
        event.callback.payload
    )
    print("=" * 50)



    await event.answer()


    await context.clear()



    # ==================================================
    # Получаем топ акции рынка
    # ==================================================

    from app.services.analysis_stocks_service import (
        AnalysisStocksService
    )


    stocks_service = AnalysisStocksService()


    try:

        result = await stocks_service.analyze_stocks(
            period=7
        )


    except Exception as e:

        print(
            "HOME MARKET ANALYSIS ERROR:",
            e
        )

        result = {
            "stocks_growth": [],
            "stocks_fall": []
        }



    text = format_market_summary(
        result
    )



    from app.keyboards.general_menu import (
        main_menu
    )


    await event.message.answer(

        text,

        attachments=[

            main_menu()

        ]

    )



# ==================================================
# Формирование текста
# ==================================================

def format_market_summary(
        result
):


    text = (
        "🏠 Главное меню\n\n"
    )


    growth = result.get(
        "stocks_growth",
        []
    )


    fall = result.get(
        "stocks_fall",
        []
    )



    # =====================================
    # Рост
    # =====================================

    text += (
        "📈 ТОП 5 роста за 7 дней:\n\n"
    )


    if growth:


        for index, item in enumerate(
                growth,
                start=1
        ):

            text += (

                f"{index}. "
                f"{item['ticker']} "
                f"+{item['change_percent']:.2f}%\n"

            )


    else:

        text += (
            "Нет данных\n"
        )



    text += "\n"



    # =====================================
    # Падение
    # =====================================

    text += (
        "📉 ТОП 5 падения за 7 дней:\n\n"
    )


    if fall:


        for index, item in enumerate(
                fall,
                start=1
        ):

            text += (

                f"{index}. "
                f"{item['ticker']} "
                f"{item['change_percent']:.2f}%\n"

            )


    else:

        text += (
            "Нет данных\n"
        )



    text += (

        "\nВыберите действие:"

    )


    return text