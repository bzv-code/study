from maxapi import Router
from maxapi.types import MessageCallback
from maxapi.context.base import BaseContext


from app.payloads.callback_payloads import (
    OrdersPayload,
    DeleteOrderPayload
)

from app.services.limit_orders_service import (
    LimitOrdersService
)

from app.keyboards.orders_menu import (
    orders_menu
)



print(
    "ORDERS CALLBACK LOADED"
)



router = Router()



limit_orders_service = LimitOrdersService()



# ==================================================
# ОБЩИЙ ВЫВОД СПИСКА ЗАЯВОК
# ==================================================

async def send_orders_list(

        event,

        user_id: int

):


    orders = await limit_orders_service.get_active_orders(

        user_id

    )



    if not orders:


        text = (

            "📋 Лимитные заявки\n\n"

            "📂 Активных заявок нет"

        )


    else:


        text = (

            "📋 Лимитные заявки\n\n"

        )


        for index, order in enumerate(

                orders,

                start=1

        ):


            text += (

                f"{index}. 📈 {order['ticker']}\n"

                f"   Количество: {order['quantity']:.2f} шт.\n"

                f"   🎯 Цена: {order['limit_price']:.2f} ₽\n"

                f"   📅 Создана: "

                f"{order['created_at'].strftime('%d.%m.%Y %H:%M')}\n\n"

            )


        text += (

            "Нажмите кнопку, чтобы удалить заявку:"

        )



    await event.message.answer(

        text,

        attachments=[

            orders_menu(orders)

        ]

    )



# ==================================================
# ИСТОРИЯ ОРДЕРОВ
# ==================================================

@router.message_callback(

    OrdersPayload.filter()

)
async def orders_callback(

        event: MessageCallback,

        context: BaseContext

):


    print("=" * 50)

    print(
        "ORDERS CALLBACK"
    )

    print("=" * 50)



    await event.answer()



    user_id = event.from_user.user_id



    await send_orders_list(

        event,

        user_id

    )



# ==================================================
# УДАЛЕНИЕ ЗАЯВКИ
# ==================================================

@router.message_callback(

    DeleteOrderPayload.filter()

)
async def delete_order_callback(

        event: MessageCallback,

        context: BaseContext

):


    await event.answer()



    user_id = event.from_user.user_id



    payload = event.callback.payload


    order_id = None


    if "|" in payload:


        _, raw_id = payload.split(

            "|",

            1

        )


        try:

            order_id = int(raw_id)

        except ValueError:

            order_id = None



    if order_id is None:


        await event.message.answer(

            "❌ Ошибка удаления заявки"

        )


        return



    deleted = await limit_orders_service.delete_order(

        user_id=user_id,

        order_id=order_id

    )



    print(

        "ORDER DELETE:",

        order_id,

        deleted

    )



    # обновляем список заявок

    await send_orders_list(

        event,

        user_id

    )