from maxapi import Router, F
from maxapi.types import MessageCreated
from maxapi.context.base import BaseContext


from app.states.user import UserStates

from app.services.portfolio_service import PortfolioService



print(
    "PORTFOLIO SELL QUOTES HANDLER LOADED"
)



router = Router()


portfolio_service = PortfolioService()





@router.message_created(

    UserStates.WAIT_SELL_TICKER,

    F.message.body.text

)
async def portfolio_sell_quotes_handler(

        event: MessageCreated,

        context: BaseContext

):


    print("=" * 50)

    print(
        "PORTFOLIO SELL TICKER HANDLER"
    )

    print("=" * 50)



    state = await context.get_state()


    print(
        "STATE:",
        state
    )



    if not event.message.body or not event.message.body.text:


        await event.message.answer(

            "❌ Введите тикер акции"

        )

        return





    ticker = (

        event.message.body.text

        .strip()

        .upper()

    )



    print(
        "SELL TICKER INPUT:",
        ticker
    )





    user_id = event.from_user.user_id





    portfolio = await portfolio_service.get_portfolio(

        user_id=user_id

    )





    position = next(

        (

            item

            for item in portfolio

            if item["ticker"] == ticker

        ),

        None

    )





    if not position:


        await event.message.answer(

            f"""
❌ Акция не найдена в портфеле


📈 {ticker}


Введите тикер из списка портфеля

"""

        )

        return






    print(

        "SELL POSITION:",

        position

    )







    # ==========================================
    # Сохраняем данные сделки
    # ==========================================


    await context.update_data(

        sell_ticker=ticker,

        sell_quantity_max=position["quantity"],

        sell_buy_price=position["buy_price"],

        sell_current_price=position["current_price"]

    )





    await context.set_state(

        UserStates.WAIT_SELL_QUANTITY

    )





    print(

        "SELL DATA SAVED"

    )



    print(

        await context.get_data()

    )





    print(

        "STATE ->",

        await context.get_state()

    )







    await event.message.answer(

        f"""
📉 Продажа {ticker}


В портфеле:

{position['quantity']:.2f} шт.


Цена покупки:

{position['buy_price']:.2f} ₽


Текущая цена:

{position['current_price']:.2f} ₽


Введите количество для продажи:


Например:
10

"""

    )