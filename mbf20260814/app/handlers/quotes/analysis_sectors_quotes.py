from maxapi import Router

from maxapi.types import MessageCreated
from maxapi.context.base import BaseContext


from app.services.analysis_sectors_service import (
    AnalysisSectorsService
)


from app.utils.analysis_sectors_formatter import (
    AnalysisSectorsFormatter
)


from app.states.user import UserStates



print(
    "ANALYSIS SECTORS QUOTES LOADED"
)



router = Router()



service = AnalysisSectorsService()



@router.message_created(

    UserStates.WAIT_ANALYSIS_SECTORS_PERIOD

)

async def analysis_sectors_quotes_handler(

        event: MessageCreated,

        context: BaseContext

):


    data = await context.get_data()



    period = data.get(

        "analysis_sectors_period",

        7

    )



    print(

        "SECTORS ANALYSIS PERIOD:",

        period

    )



    result = await service.analyze_sectors(

        period=period

    )



    if not result:


        await event.message.answer(

            "❌ Нет данных по секторам"

        )


        await context.clear()


        return



    result["period"] = period



    text = AnalysisSectorsFormatter.format(

        result

    )



    await event.message.answer(

        text

    )



    await context.clear()



    print(

        "SECTORS ANALYSIS SENT"

    )