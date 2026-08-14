from maxapi import Router

from maxapi.types import MessageCallback
from maxapi.context.base import BaseContext


from app.payloads.callback_payloads import (
    AnalysisStocksPeriodPayload
)


from app.states.user import UserStates


from app.services.analysis_stocks_service import (
    AnalysisStocksService
)


from app.utils.analysis_stocks_formatter import (
    AnalysisStocksFormatter
)


from app.keyboards.analysis_stocks_period_menu import (
    analysis_stocks_period_menu
)



print(
    "ANALYSIS STOCKS PERIOD CALLBACK LOADED"
)



router = Router()



stocks_service = AnalysisStocksService()



# ==================================================
# ПЕРИОД АНАЛИЗА АКЦИЙ
# ==================================================


@router.message_callback(

    AnalysisStocksPeriodPayload.filter()

)

async def analysis_stocks_period_callback(

        event: MessageCallback,

        context: BaseContext

):


    print("=" * 50)

    print(
        "ANALYSIS STOCKS PERIOD CALLBACK"
    )

    print(
        "PAYLOAD:",
        event.callback.payload
    )

    print("=" * 50)



    await event.answer()



    payload = event.callback.payload



    if "|" not in payload:


        await event.message.answer(

            "❌ Ошибка выбора периода"

        )

        return



    _, period_value = payload.split(

        "|",

        1

    )



    try:

        period = int(period_value)


    except ValueError:


        await event.message.answer(

            "❌ Некорректный период"

        )

        return



    print(

        "STOCKS ANALYSIS PERIOD:",

        period

    )



    try:


        # ==================================================
        # Получаем анализ акций
        # ==================================================

        result = await stocks_service.analyze_stocks(

            period=period

        )



        print(

            "STOCKS ANALYSIS RESULT:",

            result

        )



        if not result:


            await event.message.answer(

                "❌ Нет данных для анализа акций"

            )

            return



        # ==================================================
        # Форматирование
        # ==================================================

        text = AnalysisStocksFormatter.format_stocks_analysis(

            result

        )



        # ==================================================
        # Отправка результата + кнопки
        # ==================================================

        await event.message.answer(

            text,

            attachments=[

                analysis_stocks_period_menu()

            ]

        )


        print(

            "STOCKS ANALYSIS SENT"

        )


    except Exception as e:


        print(

            "STOCKS PERIOD ANALYSIS ERROR:",

            e

        )


        await event.message.answer(

            "❌ Ошибка анализа акций"

        )



    # ==================================================
    # Оставляем пользователя в меню анализа акций
    # ==================================================

    await context.set_state(

        UserStates.WAIT_ANALYSIS_STOCKS_PERIOD

    )