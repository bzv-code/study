from maxapi import Router

from maxapi.types import MessageCallback
from maxapi.context.base import BaseContext


from app.payloads.callback_payloads import (
    AnalysisPayload
)


from app.keyboards.analysis_general_menu import (
    analysis_general_menu
)



router = Router()


print(
    "ANALYSIS CALLBACK LOADED"
)



# ==================================================
# ОБЩЕЕ МЕНЮ АНАЛИЗА
# ==================================================


@router.message_callback(

    AnalysisPayload.filter()

)

async def analysis_callback(

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



    # сбрасываем старый сценарий

    await context.clear()



    # сохраняем режим

    await context.update_data(

        analysis_mode="menu"

    )



    await event.message.answer(

        """
📊 Анализ


Выберите тип анализа:

""",

        attachments=[

            analysis_general_menu()

        ]

    )