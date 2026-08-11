from maxapi.types.attachments import (
    Attachment,
    ButtonsPayload
)

from maxapi.types.attachments.buttons import (
    CallbackButton
)

from app.payloads.callback_payloads import (
    AlertConditionPayload,
    HomePayload
)


print(
    "ALERT CONDITION MENU LOADED"
)


def alert_condition_menu() -> Attachment:

    return Attachment(

        type="inline_keyboard",

        payload=ButtonsPayload(

            buttons=[

                [

                    CallbackButton(

                        text="🔼 Цена выше",

                        payload=AlertConditionPayload(

                            condition="above"

                        ).pack()

                    )

                ],

                [

                    CallbackButton(

                        text="🔽 Цена ниже",

                        payload=AlertConditionPayload(

                            condition="below"

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