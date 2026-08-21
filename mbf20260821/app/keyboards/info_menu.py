from maxapi.types.attachments import (
    Attachment,
    ButtonsPayload
)

from maxapi.types.attachments.buttons import CallbackButton


from app.payloads.callback_payloads import (
    InfoSectorsPayload,
    HomePayload
)



def info_menu():

    return Attachment(

        type="inline_keyboard",

        payload=ButtonsPayload(

            buttons=[

                [

                    CallbackButton(

                        text="📈 Акции и сектора",

                        payload=InfoSectorsPayload().pack()

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