from maxapi import Router
from maxapi.types import MessageCreated
from maxapi.context.base import BaseContext


from app.states.user import UserStates


from app.services.ticker_service import TickerService
from app.utils.ticker_formatter import formatter_quote


from app.keyboards.ticker_general_menu import quote_menu



print("TICKER QUOTES LOADED")



router = Router()


ticker_service = TickerService()



@router.message_created(
    UserStates.WAIT_TICKER
)
async def ticker_quotes_handler(
        event: MessageCreated,
        context: BaseContext
):


    print("=" * 50)
    print("TICKER HANDLER EVENT")
    print("=" * 50)



    print(
        "CHAT ID:",
        event.chat.chat_id
    )


    print(
        "USER ID:",
        event.from_user.user_id
    )



    text = ""


    if event.message.body:

        text = (
            event.message.body.text
            or ""
        )



    print(
        "MESSAGE:",
        text
    )



    # ======================================
    # Получаем состояние MAX API Context
    # ======================================

    state = await context.get_state()



    print(
        "CURRENT STATE:",
        state
    )


    print(
        "WAIT_TICKER STATE:",
        UserStates.WAIT_TICKER
    )



    # ======================================
    # Работаем только при вводе тикера
    # ======================================

    if state != UserStates.WAIT_TICKER:


        print(
            "STATE NOT MATCH - EXIT"
        )


        return



    ticker = text.strip().upper()



    if not ticker:


        await event.message.answer(

            "❌ Введите тикер акции"

        )


        return



    print(
        "TICKER RECEIVED:",
        ticker
    )



    quote = await ticker_service.get_quote(

        ticker

    )



    print(
        "MARKET RESPONSE:",
        quote
    )



    if not quote:


        await event.message.answer(

            f"❌ Тикер {ticker} не найден"

        )


        return



    # ======================================
    # Сохраняем выбранную акцию
    # ======================================

    await context.update_data(

        ticker=ticker

    )



    print(
        "CONTEXT UPDATED:",
        ticker
    )



    formatted = formatter_quote(

        quote

    )



    print(
        "FORMATTER RESULT:"
    )


    print(
        formatted
    )



    await event.message.answer(

        formatted,

        attachments=[

            quote_menu()

        ]

    )



    print(
        "QUOTE MESSAGE SENT"
    )



    await context.set_state(

        UserStates.QUOTE_MENU

    )



    print(
        "STATE CHANGED:",
        UserStates.QUOTE_MENU
    )


    print("=" * 50)