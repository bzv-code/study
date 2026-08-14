from maxapi import Router
from maxapi.context.base import BaseContext
from maxapi.types import MessageCallback

from app.states.user import UserStates
from app.payloads.callback_payloads import QuotePayload


print("QUOTE CALLBACK LOADED")


router = Router()


@router.message_callback(
    QuotePayload.filter()
)
async def quote_callback(
        event: MessageCallback,
        payload: QuotePayload,
        context: BaseContext
):

    print("==============================")
    print("QUOTE CALLBACK")
    print(
        "PAYLOAD:",
        event.callback.payload
    )
    print("==============================")


    await event.answer()


    await context.set_state(
        UserStates.WAIT_TICKER
    )


    print(
        "STATE:",
        await context.get_state()
    )


    await event.message.answer(

        "📈 Введите тикер акции:\n\n"
        "GAZP\n"
        "SBER\n"
        "LKOH"

    )