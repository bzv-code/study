from maxapi import Router

from maxapi.types import MessageCallback
from maxapi.context.base import BaseContext


from app.payloads.callback_payloads import (
    AnalysisTickerPayload
)


from app.states.user import UserStates



router = Router()



print(
    "ANALYSIS TICKER CALLBACK LOADED"
)





# ==================================================
# АНАЛИЗ ТИКЕТА
# ==================================================


@router.message_callback(

    AnalysisTickerPayload.filter()

)

async def analysis_ticker_callback(

        event: MessageCallback,

        context: BaseContext

):


    print("=" * 50)

    print(
        "ANALYSIS TICKER CALLBACK"
    )

    print(
        "PAYLOAD:",
        event.callback.payload
    )

    print("=" * 50)



    await event.answer()



    await context.clear()



    await context.update_data(

        analysis_mode="ticker"

    )



    await context.set_state(

        UserStates.WAIT_ANALYSIS_TICKER

    )

    await event.message.answer(
        "📉 Анализ тикета\n\n"
        "Введите тикер акции:\n"
        "Например:\n"
        "GAZP\n"
        "SBER\n"
        "LKOH"
    )



    print(

        "STATE -> WAIT_ANALYSIS_TICKER"

    )