from maxapi import Router

from maxapi.types import MessageCreated
from maxapi.context.base import BaseContext


from app.services.analysis_stocks_service import (
    AnalysisStocksService
)


from app.utils.analysis_stocks_formatter import (
    AnalysisStocksFormatter
)


from app.states.user import UserStates



print(
    "ANALYSIS STOCKS QUOTES LOADED"
)


router = Router()


service = AnalysisStocksService()



# ==================================================
# АНАЛИЗ АКЦИЙ
# ==================================================


@router.message_created(

    UserStates.WAIT_ANALYSIS_STOCKS_PERIOD

)

async def analysis_stocks_quotes_handler(

        event: MessageCreated,

        context: BaseContext

):


    data = await context.get_data()


    period = data.get(

        "analysis_stocks_period",

        7

    )



    print(

        "STOCKS ANALYSIS PERIOD:",

        period

    )



    result = await service.analyze_stocks(

        period=period

    )



    if not result:


        await event.message.answer(

            "❌ Нет данных по акциям"

        )

        await context.clear()

        return



    result["period"] = period



    text = AnalysisStocksFormatter.format(

        result

    )



    await event.message.answer(

        text

    )



    await context.clear()



    print(

        "STOCKS ANALYSIS SENT"

    )