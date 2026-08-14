from maxapi.types.attachments import (
    Attachment,
    ButtonsPayload
)

from maxapi.types.attachments.buttons import (
    CallbackButton
)


from app.payloads.callback_payloads import (
    AnalysisTickerPayload,
    AnalysisStocksPayload,
    AnalysisSectorsPayload,
    HomePayload
)



def analysis_general_menu():

    return Attachment(

        type="inline_keyboard",

        payload=ButtonsPayload(

            buttons=[


                # =====================================
                # Анализ одной акции
                # =====================================

                [

                    CallbackButton(

                        text="📉 Анализ тикета",

                        payload=AnalysisTickerPayload().pack()

                    )

                ],



                # =====================================
                # Анализ всех акций
                # =====================================

                [

                    CallbackButton(

                        text="📈 Анализ акций",

                        payload=AnalysisStocksPayload().pack()

                    )

                ],



                # =====================================
                # Анализ секторов
                # =====================================

                [

                    CallbackButton(

                        text="🏭 Анализ секторов",

                        payload=AnalysisSectorsPayload().pack()

                    )

                ],



                # =====================================
                # Главное меню
                # =====================================

                [

                    CallbackButton(

                        text="⬅️ Главное меню",

                        payload=HomePayload().pack()

                    )

                ]

            ]

        )

    )