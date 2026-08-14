from maxapi import Router

from maxapi.types import MessageCallback
from maxapi.context.base import BaseContext


from app.payloads.callback_payloads import (
    AnalysisStocksPayload
)


from app.states.user import UserStates


from app.keyboards.analysis_stocks_period_menu import (
    analysis_stocks_period_menu
)


from app.services.analysis_stocks_service import (
    AnalysisStocksService
)


from app.utils.analysis_stocks_formatter import (
    AnalysisStocksFormatter
)



router = Router()


print(
    "ANALYSIS STOCKS CALLBACK LOADED"
)



service = AnalysisStocksService()



# ==================================================
# ОТКРЫТИЕ АНАЛИЗА АКЦИЙ
# ==================================================


@router.message_callback(

    AnalysisStocksPayload.filter()

)
async def analysis_stocks_callback(

        event: MessageCallback,

        context: BaseContext

):


    print("=" * 50)

    print(
        "ANALYSIS STOCKS CALLBACK"
    )

    print(
        "PAYLOAD:",
        event.callback.payload
    )

    print("=" * 50)



    await event.answer()



    # ==================================================
    # Сброс старого состояния
    # ==================================================

    await context.clear()



    # ==================================================
    # Сохраняем режим
    # ==================================================

    await context.update_data(

        analysis_mode="stocks"

    )

    # ==================================================
    # Автоматический анализ за 1 день
    # ==================================================

    try:

        result = await service.analyze_stocks(

            period=1

        )

        text = AnalysisStocksFormatter.format_stocks_analysis(

            result

        )

        await event.message.answer(

            text,

            attachments=[

                analysis_stocks_period_menu()

            ]

        )

        print(

            "DEFAULT STOCKS ANALYSIS SENT"

        )



    except Exception as e:

        print(

            "ANALYSIS STOCKS ERROR:",

            e

        )

        await event.message.answer(

            "❌ Ошибка анализа акций"

        )



    # ==================================================
    # Оставляем состояние для кнопок периода
    # ==================================================

    await context.set_state(

        UserStates.WAIT_ANALYSIS_STOCKS_PERIOD

    )



    print(

        "STATE -> WAIT_ANALYSIS_STOCKS_PERIOD"

    )