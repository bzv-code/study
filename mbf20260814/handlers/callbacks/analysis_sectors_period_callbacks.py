from maxapi import Router


from maxapi.types import MessageCallback
from maxapi.context.base import BaseContext


from app.payloads.callback_payloads import (
    AnalysisSectorsPeriodPayload
)


from app.states.user import UserStates


from app.services.analysis_sectors_service import (
    AnalysisSectorsService
)


from app.utils.analysis_sectors_formatter import (
    AnalysisSectorsFormatter
)


from app.keyboards.analysis_sectors_period_menu import (
    analysis_sectors_period_menu
)



print(
    "ANALYSIS SECTORS PERIOD CALLBACK LOADED"
)



router = Router()



service = AnalysisSectorsService()



# ==================================================
# ПЕРИОД АНАЛИЗА СЕКТОРОВ
# ==================================================


@router.message_callback(

    AnalysisSectorsPeriodPayload.filter()

)

async def analysis_sectors_period_callback(

        event: MessageCallback,

        context: BaseContext

):


    print("=" * 50)

    print(
        "ANALYSIS SECTORS PERIOD CALLBACK"
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

        "SECTORS PERIOD:",

        period

    )



    try:


        # ==================================================
        # Анализ секторов
        # ==================================================

        result = await service.analyze_sectors(

            period=period

        )



        print(

            "SECTORS RESULT:",

            result

        )



        if not result:


            await event.message.answer(

                "❌ Нет данных по секторам"

            )

            return



        # ==================================================
        # Добавляем период для formatter
        # ==================================================

        result["period"] = period



        text = AnalysisSectorsFormatter.format(

            result

        )



        # ==================================================
        # Отправка результата + кнопки
        # ==================================================

        await event.message.answer(

            text,

            attachments=[

                analysis_sectors_period_menu()

            ]

        )



        print(

            "SECTORS ANALYSIS SENT"

        )


    except Exception as e:


        print(

            "SECTORS PERIOD ERROR:",

            e

        )


        await event.message.answer(

            "❌ Ошибка анализа секторов"

        )



    # ==================================================
    # Оставляем пользователя в меню секторов
    # ==================================================

    await context.set_state(

        UserStates.WAIT_ANALYSIS_SECTORS_PERIOD

    )