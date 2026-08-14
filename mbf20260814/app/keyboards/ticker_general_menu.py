from maxapi.types.attachments import (
    Attachment,
    ButtonsPayload
)

from maxapi.types.attachments.buttons import (
    CallbackButton
)


from app.payloads.callback_payloads import (
    HistoryPayload,
    ChartPayload,
    CreateAlertFromQuotePayload,
    AddPortfolioPayload,
    HomePayload
)



print(
    "TICKER GENERAL MENU LOADED"
)



def quote_menu() -> Attachment:


    return Attachment(

        type="inline_keyboard",

        payload=ButtonsPayload(

            buttons=[


                # =====================================
                # История + График
                # =====================================

                [

                    CallbackButton(

                        text="📈 История",

                        payload=HistoryPayload().pack()

                    ),


                    CallbackButton(

                        text="📊 График",

                        payload=ChartPayload().pack()

                    )

                ],



                # =====================================
                # Уведомление выбранного тикера
                # =====================================

                [

                    CallbackButton(

                        text="➕ Создать уведомление",

                        payload=CreateAlertFromQuotePayload().pack()

                    )

                ],



                # =====================================
                # Добавить в портфель
                # =====================================

                [

                    CallbackButton(

                        text="➕ Добавить в портфель",

                        payload=AddPortfolioPayload().pack()

                    )

                ],



                # =====================================
                # Главное меню
                # =====================================

                [

                    CallbackButton(

                        text="⬅️ Главное меню",

                        payload=HomePayload().pack()

                    )

                ]

            ]

        )

    )