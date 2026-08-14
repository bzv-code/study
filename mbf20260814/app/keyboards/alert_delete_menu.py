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


def alert_my_alerts_menu(alerts: list = None):

    buttons = []

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
        payload=ButtonsPayload(buttons=buttons)
    )