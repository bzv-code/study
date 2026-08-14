from maxapi.types.attachments import (
    Attachment,
    ButtonsPayload
)

from maxapi.types.attachments.buttons import CallbackButton


from app.payloads.callback_payloads import (

    AddPortfolioFromMenuPayload,

    SellPortfolioPayload,

    DeletePortfolioPayload,

    HistoryPayload,

    ClearHistoryPayload,

    HomePayload

)



def portfolio_menu():


    return Attachment(


        type="inline_keyboard",


        payload=ButtonsPayload(


            buttons=[


                [

                    CallbackButton(

                        text="➕ Добавить акцию",

                        payload=AddPortfolioFromMenuPayload().pack()

                    )

                ],



                [

                    CallbackButton(

                        text="📉 Продать акцию",

                        payload=SellPortfolioPayload().pack()

                    )

                ],



                [

                    CallbackButton(

                        text="❌ Удалить акцию",

                        payload=DeletePortfolioPayload().pack()

                    )

                ],



                [

                    CallbackButton(

                        text="📜 История сделок",

                        payload=HistoryPayload().pack()

                    )

                ],



                [

                    CallbackButton(

                        text="🗑 Очистить историю",

                        payload=ClearHistoryPayload().pack()

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