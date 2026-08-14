from maxapi import Router, F
from maxapi.types import MessageCreated
from maxapi.context.base import BaseContext


from app.states.user import UserStates



print(
    "PORTFOLIO SELL QUANTITY HANDLER LOADED"
)



router = Router()





@router.message_created(

    UserStates.WAIT_SELL_QUANTITY,

    F.message.body.text

)
async def portfolio_sell_quantity_handler(

        event: MessageCreated,

        context: BaseContext

):


    print("=" * 50)

    print(
        "PORTFOLIO SELL QUANTITY HANDLER"
    )

    print("=" * 50)




    state = await context.get_state()


    print(
        "STATE:",
        state
    )





    if not event.message.body or not event.message.body.text:


        await event.message.answer(

            "❌ Введите количество акций"

        )

        return





    text = (

        event.message.body.text

        .strip()

        .replace(",", ".")

    )



    try:

        quantity = float(text)


    except ValueError:


        await event.message.answer(

            """
❌ Неверное количество


Введите число:

Например:
10
"""

        )

        return





    data = await context.get_data()



    print(
        "SELL DATA:",
        data
    )





    max_quantity = data.get(

        "sell_quantity_max"

    )


    ticker = data.get(

        "sell_ticker"

    )


    buy_price = data.get(

        "sell_buy_price"

    )





    if (

        max_quantity is None

        or ticker is None

        or buy_price is None

    ):


        print(

            "SELL DATA ERROR",

            {

                "max_quantity": max_quantity,

                "ticker": ticker,

                "buy_price": buy_price

            }

        )


        await event.message.answer(

            "❌ Ошибка данных продажи. Начните продажу заново."

        )


        await context.clear()


        return






    if quantity <= 0:


        await event.message.answer(

            "❌ Количество должно быть больше 0"

        )

        return






    if quantity > max_quantity:


        await event.message.answer(

            f"""
❌ Нельзя продать больше имеющихся акций


📈 {ticker}


В портфеле:
{max_quantity:.2f} шт.


Введите меньшее количество

"""

        )

        return






    await context.update_data(

        sell_quantity=quantity

    )





    await context.set_state(

        UserStates.WAIT_SELL_PRICE

    )





    print(

        "SAVE SELL QUANTITY:",

        quantity

    )


    print(

        "STATE ->",

        await context.get_state()

    )





    await event.message.answer(

        f"""
📉 Продажа {ticker}


Количество:
{quantity:.2f} шт.


Цена покупки:
{buy_price:.2f} ₽


Введите цену продажи:

Например:
270.50
"""

    )