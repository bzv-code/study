from maxapi import Router

from maxapi.types import MessageCallback
from maxapi.context.base import BaseContext


from app.payloads.callback_payloads import (
    AnalysisSectorsPayload
)


from app.states.user import UserStates


from app.keyboards.analysis_sectors_period_menu import (
    analysis_sectors_period_menu
)


from app.services.analysis_sectors_service import (
    AnalysisSectorsService
)


from app.utils.analysis_sectors_formatter import (
    AnalysisSectorsFormatter
)



print(
    "ANALYSIS SECTORS CALLBACK LOADED"
)



router = Router()



service = AnalysisSectorsService()



# ==================================================
# ОТКРЫТИЕ АНАЛИЗА СЕКТОРОВ
# ==================================================


@router.message_callback(

    AnalysisSectorsPayload.filter()

)

async def analysis_sectors_callback(

        event: MessageCallback,

        context: BaseContext

):


    print("=" * 50)

    print(
        "ANALYSIS SECTORS CALLBACK"
    )

    print(
        "PAYLOAD:",
        event.callback.payload
    )

    print("=" * 50)



    await event.answer()



    # ==================================================
    # Очистка старого сценария
    # ==================================================

    await context.clear()



    # ==================================================
    # Сохраняем режим
    # ==================================================

    await context.update_data(

        analysis_mode="sectors"

    )



    try:


        # ==================================================
        # Автоматический анализ за 1 день
        # ==================================================

        result = await service.analyze_sectors(

            period=1

        )



        print(

            "SECTORS ANALYSIS RESULT:",

            result

        )



        text = AnalysisSectorsFormatter.format(

            result

        )



        await event.message.answer(

            text,

            attachments=[

                analysis_sectors_period_menu()

            ]

        )



        print(

            "DEFAULT SECTORS ANALYSIS SENT"

        )



    except Exception as e:


        print(

            "ANALYSIS SECTORS ERROR:",

            e

        )


        await event.message.answer(

            "❌ Ошибка анализа секторов"

        )



    # ==================================================
    # Оставляем состояние для кнопок периода
    # ==================================================

    await context.set_state(

        UserStates.WAIT_ANALYSIS_SECTORS_PERIOD

    )



    print(

        "STATE -> WAIT_ANALYSIS_SECTORS_PERIOD"

    )