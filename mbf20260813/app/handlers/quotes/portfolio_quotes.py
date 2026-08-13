from maxapi import Router, F
from maxapi.types import MessageCreated
from maxapi.context.base import BaseContext

from app.states.user import UserStates

from app.services.ticker_service import TickerService



print(
    "PORTFOLIO QUOTES HANDLER LOADED"
)



router = Router()


ticker_service = TickerService()




from maxapi import F


@router.message_created(
    UserStates.WAIT_PORTFOLIO_TICKER,
    F.message.body.text
)
async def portfolio_quotes_handler(
    event: MessageCreated,
    context: BaseContext
):


    print("=" * 50)
    print("PORTFOLIO QUOTES HANDLER EVENT")
    print("=" * 50)



    state = await context.get_state()



    print(
        "CURRENT STATE:",
        state
    )



    # ==================================================
    # Работаем только когда пользователь вводит тикер
    # после:
    #
    # Портфель -> Добавить акцию
    #
    # ==================================================

    if state != UserStates.WAIT_PORTFOLIO_TICKER:


        print(
            "PORTFOLIO QUOTES STATE NOT MATCH"
        )


        return




    if not event.message.body:


        print(
            "EMPTY MESSAGE BODY"
        )


        return




    if not event.message.body.text:


        print(
            "EMPTY MESSAGE TEXT"
        )


        return




    ticker = (

        event.message.body.text

        .strip()

        .upper()

    )



    print(
        "PORTFOLIO TICKER INPUT:",
        ticker
    )



    if not ticker:


        await event.message.answer(

            "❌ Введите тикер акции"

        )


        return




    # ==================================================
    # Проверяем существование акции
    # ==================================================

    quote = await ticker_service.get_quote(

        ticker

    )



    print(
        "QUOTE RESULT:",
        quote
    )



    if not quote:


        await event.message.answer(

            f"❌ Акция {ticker} не найдена\n\n"
            "Введите корректный тикер"

        )


        return




    # ==================================================
    # Сохраняем тикер
    # ==================================================

    await context.update_data(

        portfolio_ticker=ticker

    )



    await context.set_state(

        UserStates.WAIT_PORTFOLIO_QUANTITY

    )



    print(
        "PORTFOLIO TICKER SAVED:",
        ticker
    )



    print(
        "STATE ->",
        UserStates.WAIT_PORTFOLIO_QUANTITY
    )




    await event.message.answer(

        f"➕ Добавление {ticker}\n\n"

        "Введите количество акций:\n\n"

        "Например:\n"

        "10"

    )