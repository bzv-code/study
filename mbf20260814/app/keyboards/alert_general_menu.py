from maxapi.types.attachments import (
    Attachment,
    ButtonsPayload
)

from maxapi.types.attachments.buttons import (
    CallbackButton
)

from app.payloads.callback_payloads import (
    CreateAlertPayload,
    DeleteAlertPayload,
    HomePayload
)


print(
    "ALERT GENERAL MENU LOADED"
)



def alert_general_menu(
        alerts=None
) -> Attachment:


    buttons = []



    # =====================================
    # Кнопки удаления уведомлений
    # =====================================

    if alerts:


        for alert in alerts:


            buttons.append(

                [

                    CallbackButton(

                        text=f"🗑 Удалить {alert.ticker}",

                        payload=DeleteAlertPayload(

                            alert_id=alert.id

                        ).pack()

                    )

                ]

            )



    # =====================================
    # Общие кнопки
    # =====================================

    buttons.extend(

        [

            [

                CallbackButton(

                    text="➕ Создать уведомление",

                    payload=CreateAlertPayload().pack()

                )

            ],


            [

                CallbackButton(

                    text="🏠 Главное меню",

                    payload=HomePayload().pack()

                )

            ]

        ]

    )



    return Attachment(

        type="inline_keyboard",

        payload=ButtonsPayload(

            buttons=buttons

        )

    )



# ==================================================
# СОВМЕСТИМОСТЬ СО СТАРЫМ КОДОМ
# ==================================================

def price_alert_menu(
        alerts=None
) -> Attachment:


    return alert_general_menu(
        alerts
    )