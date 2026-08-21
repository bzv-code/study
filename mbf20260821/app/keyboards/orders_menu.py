from maxapi.types.attachments import (
    Attachment,
    ButtonsPayload
)

from maxapi.types.attachments.buttons import CallbackButton


from app.payloads.callback_payloads import (
    DeleteOrderPayload,
    PortfolioPayload
)



def orders_menu(orders):

    buttons = []



    # =====================================
    # Кнопки удаления заявок
    # =====================================

    for order in orders:

        buttons.append(

            [

                CallbackButton(

                    text=(

                        f"❌ №{order['id']} "

                        f"{order['ticker']} "

                        f"@ {order['limit_price']:.2f} ₽"

                    ),

                    payload=DeleteOrderPayload(

                        order_id=order["id"]

                    ).pack()

                )

            ]

        )



    # =====================================
    # Кнопка возврата в портфель
    # =====================================

    buttons.append(

        [

            CallbackButton(

                text="⬅️ К портфелю",

                payload=PortfolioPayload().pack()

            )

        ]

    )



    return Attachment(

        type="inline_keyboard",

        payload=ButtonsPayload(

            buttons=buttons

        )

    )