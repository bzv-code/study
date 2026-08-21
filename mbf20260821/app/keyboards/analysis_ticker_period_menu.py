from maxapi.types.attachments import (
    Attachment,
    ButtonsPayload
)

from maxapi.types.attachments.buttons import (
    CallbackButton
)


from app.payloads.callback_payloads import (
    AnalysisPeriodPayload,
    HomePayload
)



def analysis_ticker_period_menu():

    return Attachment(

        type="inline_keyboard",

        payload=ButtonsPayload(

            buttons=[

                [

                    CallbackButton(
                        text="📅 7 дней",
                        payload=AnalysisPeriodPayload(
                            period="7"
                        ).pack()
                    )

                ],


                [

                    CallbackButton(
                        text="📅 14 дней",
                        payload=AnalysisPeriodPayload(
                            period="14"
                        ).pack()
                    )

                ],


                [

                    CallbackButton(
                        text="📅 30 дней",
                        payload=AnalysisPeriodPayload(
                            period="30"
                        ).pack()
                    )

                ],


                [

                    CallbackButton(
                        text="📅 180 дней",
                        payload=AnalysisPeriodPayload(
                            period="180"
                        ).pack()
                    )

                ],


                [

                    CallbackButton(
                        text="⬅️ Главное меню",
                        payload=HomePayload().pack()
                    )

                ]

            ]

        )

    )