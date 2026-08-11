from maxapi import Router

from maxapi.types import MessageCallback
from maxapi.context.base import BaseContext


from app.states.user import UserStates


from app.payloads.callback_payloads import (
    AlertsPayload,
    CreateAlertPayload,
    DeleteAlertPayload,
)


from app.services.alert_service import (
    AlertService,
)


from app.keyboards.alert_general_menu import (
    alert_general_menu,
)


print(
    "ALERT CALLBACK LOADED"
)


router = Router()


alert_service = AlertService()



# ==================================================
# ФОРМАТИРОВАНИЕ УВЕДОМЛЕНИЙ
# ==================================================

def format_alerts_text(alerts):

    if not alerts:

        return (
            "📋 Мои уведомления\n\n"
            "У вас пока нет уведомлений."
        )


    text = (
        "📋 Мои уведомления\n\n"
    )


    for index, alert in enumerate(
            alerts,
            start=1
    ):

        condition = (
            "Цена выше"
            if alert.condition == "above"
            else "Цена ниже"
        )


        status = (
            "🟢 Активно"
            if alert.is_active
            else "⚪ Неактивно"
        )


        text += (

            f"{index}. {alert.ticker}\n"

            f"{condition}: "
            f"{alert.target_price:.2f} ₽\n"

            f"{status}\n\n"

        )


    return text




# ==================================================
# КНОПКА "УВЕДОМЛЕНИЯ"
# ==================================================

@router.message_callback(
    AlertsPayload.filter()
)
async def alerts_callback(
        event: MessageCallback,
        context: BaseContext
):


    print("=" * 50)
    print("ALERTS CALLBACK")
    print(
        event.callback.payload
    )
    print("=" * 50)


    await event.answer()


    await context.clear()


    user_id = event.from_user.user_id


    alerts = alert_service.get_user_alerts(

        user_id

    )


    await event.message.answer(

        format_alerts_text(alerts),

        attachments=[

            alert_general_menu(alerts)

        ]

    )



# ==================================================
# СОЗДАТЬ УВЕДОМЛЕНИЕ
# ==================================================

@router.message_callback(
    CreateAlertPayload.filter()
)
async def create_alert_callback(
        event: MessageCallback,
        context: BaseContext
):


    print(
        "CREATE ALERT CALLBACK"
    )


    await event.answer()


    data = await context.get_data()


    print(
        "CREATE ALERT CONTEXT:",
        data
    )



    ticker = data.get(
        "ticker"
    )


    quote_context = data.get(

        "quote_context"

    )



    # ==================================================
    # Сценарий из КОТИРОВКИ
    # ==================================================

    if ticker and quote_context is True:


        await context.update_data(

            alert_ticker=ticker,

            alert_price=None

        )


        await context.set_state(

            UserStates.WAIT_ALERT_PRICE

        )


        await event.message.answer(

            f"""
🔔 {ticker}


Введите цену уведомления:
"""

        )


        print(
            "ALERT FROM QUOTE:",
            ticker
        )


        return



    # ==================================================
    # Сценарий из ОБЩЕГО МЕНЮ УВЕДОМЛЕНИЙ
    # ==================================================


    await context.clear()


    await context.set_state(

        UserStates.WAIT_ALERT_TICKER

    )


    await event.message.answer(

        "📈 Введите тикер акции:\n\n"

        "Например:\n"

        "GAZP\n"

        "SBER\n"

        "LKOH"

    )


    print(
        "STATE -> WAIT_ALERT_TICKER"
    )




# ==================================================
# УДАЛЕНИЕ УВЕДОМЛЕНИЯ
# ==================================================

@router.message_callback(
    DeleteAlertPayload.filter()
)
async def delete_alert_callback(
        event: MessageCallback,
        payload: DeleteAlertPayload
):


    print("=" * 50)

    print(
        "DELETE ALERT CALLBACK"
    )

    print(
        "ALERT ID:",
        payload.alert_id
    )

    print("=" * 50)



    await event.answer()



    success = alert_service.delete_alert(

        payload.alert_id

    )



    if not success:


        await event.message.answer(

            "❌ Уведомление не найдено."

        )

        return



    user_id = event.from_user.user_id



    alerts = alert_service.get_user_alerts(

        user_id

    )



    await event.message.answer(

        format_alerts_text(alerts),

        attachments=[

            alert_general_menu(alerts)

        ]

    )