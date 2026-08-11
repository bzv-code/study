from maxapi.types.attachments import (
    Attachment,
    ButtonsPayload
)

from maxapi.types.attachments.buttons import CallbackButton


from app.payloads.callback_payloads import (
    QuotePayload,
    AnalysisPayload,
    PortfolioPayload,
    AlertsPayload
)



def main_menu():

    return Attachment(

        type="inline_keyboard",

        payload=ButtonsPayload(

            buttons=[

                [

                    CallbackButton(
                        text="📈 Котировки",
                        payload=QuotePayload().pack()
                    )

                ],


                [

                    CallbackButton(
                        text="📉 Анализ",
                        payload=AnalysisPayload().pack()
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

                ]

            ]

        )

    )