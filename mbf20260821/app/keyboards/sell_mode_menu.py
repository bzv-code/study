from maxapi.types.attachments import (
    Attachment,
    ButtonsPayload
)

from maxapi.types.attachments.buttons import CallbackButton


from app.payloads.callback_payloads import (
    SellModePayload
)



def sell_mode_menu():

    return Attachment(

        type="inline_keyboard",

        payload=ButtonsPayload(

            buttons=[

                [

                    CallbackButton(

                        text="📊 По рынку",

                        payload=SellModePayload(

                            mode="market"

                        ).pack()

                    )

                ],



                [

                    CallbackButton(

                        text="⏳ Лимитная заявка",

                        payload=SellModePayload(

                            mode="limit"

                        ).pack()

                    )

                ]

            ]

        )

    )