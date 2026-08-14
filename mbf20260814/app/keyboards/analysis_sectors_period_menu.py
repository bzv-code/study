from maxapi.types.attachments import (
    Attachment,
    ButtonsPayload
)

from maxapi.types.attachments.buttons import (
    CallbackButton
)


from app.payloads.callback_payloads import (
    AnalysisSectorsPeriodPayload,
    HomePayload
)



print(
    "ANALYSIS SECTORS PERIOD MENU LOADED"
)



def analysis_sectors_period_menu():

    return Attachment(

        type="inline_keyboard",

        payload=ButtonsPayload(

            buttons=[


                [
                    CallbackButton(

                        text="📅 7 дней",

                        payload=AnalysisSectorsPeriodPayload(
                            period="7"
                        ).pack()

                    )
                ],


                [
                    CallbackButton(

                        text="📅 14 дней",

                        payload=AnalysisSectorsPeriodPayload(
                            period="14"
                        ).pack()

                    )
                ],


                [
                    CallbackButton(

                        text="📅 30 дней",

                        payload=AnalysisSectorsPeriodPayload(
                            period="30"
                        ).pack()

                    )
                ],


                [
                    CallbackButton(

                        text="📅 180 дней",

                        payload=AnalysisSectorsPeriodPayload(
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