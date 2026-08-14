from maxapi import Router

from maxapi.types import MessageCallback
from maxapi.context.base import BaseContext


from app.states.user import UserStates


from app.payloads.callback_payloads import (
    AlertConditionPayload
)


from app.services.alert_service import (
    AlertService
)


from app.keyboards.alert_general_menu import (
    alert_general_menu
)



print(
    "ALERT CONDITION CALLBACK LOADED"
)



router = Router()


alert_service = AlertService()



# ==================================================
# ВЫБОР УСЛОВИЯ УВЕДОМЛЕНИЯ
# ==================================================

@router.message_callback(
    AlertConditionPayload.filter()
)
async def alert_condition_callback(
        event: MessageCallback,
        context: BaseContext
):


    print("=" * 50)

    print(
        "ALERT CONDITION CALLBACK"
    )

    print(
        "PAYLOAD:",
        event.callback.payload
    )

    print("=" * 50)



    await event.answer()



    payload = event.callback.payload



    if "|" not in payload:


        await event.message.answer(
            "❌ Ошибка выбора условия"
        )

        return



    _, condition = payload.split(
        "|",
        1
    )



    if condition not in (
        "above",
        "below"
    ):


        await event.message.answer(
            "❌ Некорректное условие уведомления"
        )

        return



    data = await context.get_data()



    print(
        "ALERT CONTEXT:",
        data
    )



    ticker = data.get(
        "alert_ticker"
    )


    price = data.get(
        "alert_price"
    )


    source = data.get(
        "alert_source"
    )



    print(
        "SOURCE:",
        source
    )



    if not ticker:


        await event.message.answer(

            "❌ Не найден тикер акции"

        )


        await context.clear()

        return



    if price is None:


        await event.message.answer(

            "❌ Не найдена цена уведомления"

        )


        await context.clear()

        return



    # ==================================================
    # СОЗДАНИЕ УВЕДОМЛЕНИЯ
    # ==================================================

    result = await alert_service.create_alert(

        user_id=event.from_user.user_id,

        ticker=ticker,

        target_price=float(price),

        condition=condition

    )



    if not result["success"]:


        await event.message.answer(

            f"❌ {result['message']}"

        )


        return



    alert = result["alert"]



    condition_text = (

        "Цена выше"

        if condition == "above"

        else

        "Цена ниже"

    )



    # ==================================================
    # СООБЩЕНИЕ О СОЗДАНИИ
    # ==================================================

    await event.message.answer(

        f"""
✅ Уведомление создано

📈 Акция:
{alert.ticker}

💰 Цена:
{alert.target_price:.2f} ₽

Условие:
{condition_text}
"""

    )



    # ==================================================
    # УДАЛЕНО: СОЗДАНИЕ ИЗ МЕНЮ КОТИРОВКИ
    # (возврат в quote_menu больше не нужен)
    # ==================================================

    # if source == "quote":
    #     ... (код удалён)



    # ==================================================
    # СОЗДАНИЕ ИЗ ГЛАВНОГО МЕНЮ
    # ==================================================

    await context.clear()



    alerts = alert_service.get_user_alerts(

        event.from_user.user_id

    )



    await event.message.answer(

        format_alerts_text(alerts),

        attachments=[

            alert_general_menu(alerts)

        ]

    )



    print(
        "RETURN ALERT MENU"
    )



    print(

        "ALERT CREATED:",

        alert.id

    )



# ==================================================
# ФОРМАТ СПИСКА УВЕДОМЛЕНИЙ
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

            else

            "Цена ниже"

        )


        status = (

            "🟢 Активно"

            if alert.is_active

            else

            "⚪ Неактивно"

        )



        text += (

            f"{index}. {alert.ticker}\n"

            f"{condition}: "

            f"{alert.target_price:.2f} ₽\n"

            f"{status}\n\n"

        )



    return text