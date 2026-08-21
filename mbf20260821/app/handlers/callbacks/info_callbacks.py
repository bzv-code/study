from maxapi import Router

from maxapi.types import MessageCallback
from maxapi.context.base import BaseContext


from app.payloads.callback_payloads import (
    InfoPayload,
    InfoStocksPayload,
    InfoSectorsPayload
)

from app.services.info_service import InfoService

from app.keyboards.info_menu import info_menu



print(
    "INFO CALLBACK LOADED"
)



router = Router()



info_service = InfoService()



# ==================================================
# РАЗБИВКА ДЛИННОГО ТЕКСТА НА СООБЩЕНИЯ
# ==================================================

def split_text(

        text: str,

        limit: int = 3900

) -> list:


    chunks = []

    current = ""



    for line in text.split("\n"):


        if (

            current

            and len(current) + len(line) + 1 > limit

        ):

            chunks.append(current)

            current = line

        else:

            current = (

                current + "\n" + line

                if current

                else line

            )



    if current:

        chunks.append(current)



    return chunks



# ==================================================
# ГЛАВНОЕ МЕНЮ ИНФОРМАЦИИ
# ==================================================

@router.message_callback(

    InfoPayload.filter()

)
async def info_callback(

        event: MessageCallback,

        context: BaseContext

):


    print("=" * 50)

    print(
        "INFO CALLBACK"
    )

    print("=" * 50)



    await event.answer()



    await context.clear()



    await event.message.answer(

        "ℹ️ Информация\n\nВыберите раздел:",

        attachments=[

            info_menu()

        ]

    )



# ==================================================
# СПИСОК АКЦИЙ
# ==================================================

@router.message_callback(

    InfoStocksPayload.filter()

)
async def info_stocks_callback(

        event: MessageCallback,

        context: BaseContext

):


    print("=" * 50)

    print(
        "INFO STOCKS CALLBACK"
    )

    print("=" * 50)



    await event.answer()



    text = await info_service.get_stocks_text()



    for chunk in split_text(text):


        await event.message.answer(

            chunk

        )



    await event.message.answer(

        "ℹ️ Информация\n\nВыберите раздел:",

        attachments=[

            info_menu()

        ]

    )



# ==================================================
# СПИСОК СЕКТОРОВ
# ==================================================

@router.message_callback(

    InfoSectorsPayload.filter()

)
async def info_sectors_callback(

        event: MessageCallback,

        context: BaseContext

):


    print("=" * 50)

    print(
        "INFO SECTORS CALLBACK"
    )

    print("=" * 50)



    await event.answer()



    text = await info_service.get_sectors_text()



    for chunk in split_text(text):


        await event.message.answer(

            chunk

        )



    await event.message.answer(

        "ℹ️ Информация\n\nВыберите раздел:",

        attachments=[

            info_menu()

        ]

    )