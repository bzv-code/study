from maxapi.types.attachments import (
    Attachment,
    ButtonsPayload
)

from maxapi.types.attachments.buttons import CallbackButton


from app.payloads.callback_payloads import (
    AnalysisPayload,
    DividendsPayload,
    PortfolioPayload,
    AlertsPayload,
    InfoPayload
)



def main_menu():

    return Attachment(

        type="inline_keyboard",

        payload=ButtonsPayload(

            buttons=[

                [

                    CallbackButton(

                        text="📉 Анализ",

                        payload=AnalysisPayload().pack()

                    )

                ],


                [

                    CallbackButton(

                        text="💰 Дивиденды",

                        payload=DividendsPayload().pack()

                    )

                ],


                [

                    CallbackButton(

                        text="📊 Портфель",

                        payload=PortfolioPayload().pack()

                    )

                ],


                [

                    CallbackButton(

                        text="🔔 Уведомления",

                        payload=AlertsPayload().pack()

                    )

                ],


                [

                    CallbackButton(

                        text="ℹ️ Информация",

                        payload=InfoPayload().pack()

                    )

                ]

            ]

        )

    )