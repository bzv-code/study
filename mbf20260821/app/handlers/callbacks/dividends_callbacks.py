from datetime import timedelta

from maxapi import Router

from maxapi.types import MessageCallback
from maxapi.context.base import BaseContext


from app.payloads.callback_payloads import (
    DividendsPayload,
    HomePayload
)

from app.services.dividends_service import DividendsService

from app.keyboards.general_menu import main_menu


router = Router()


print(
    "DIVIDENDS CALLBACK LOADED"
)



# ==================================================
# ОБРАБОТЧИК КНОПКИ ДИВИДЕНДЫ
# ==================================================


@router.message_callback(

    DividendsPayload.filter()

)

async def dividends_callback(

        event: MessageCallback,

        context: BaseContext

):


    print("=" * 50)

    print(
        "DIVIDENDS CALLBACK"
    )

    print(
        "PAYLOAD:",
        event.callback.payload
    )

    print("=" * 50)



    await event.answer()



    # сбрасываем старый сценарий

    await context.clear()



    # ==================================================
    # Получаем будущие дивиденды
    # ==================================================

    dividends_service = DividendsService()


    try:

        dividends = await dividends_service.get_future_dividends()


    except Exception as e:

        print(
            "DIVIDENDS SERVICE ERROR:",
            e
        )

        dividends = []



    text = format_dividends(
        dividends
    )



    await event.message.answer(

        text,

        attachments=[

            main_menu()

        ]

    )



# ==================================================
# Форматирование суммы дивидендов
# ==================================================

def format_amount(amount):
    """
    Форматирует сумму дивидендов:
    - Если дробная часть = 0, выводит только целое число (200)
    - Если есть дробная часть, выводит 2 знака после запятой (2.74)
    """

    # Конвертируем в float чтобы работать с decimal.Decimal
    amount = float(amount)

    rounded = round(amount, 2)

    if rounded == int(rounded):
        return str(int(rounded))

    return f"{rounded:.2f}"

# ==================================================
# Расчет доходности
# ==================================================

def calculate_yield(dividend_amount, last_price):
    """
    Рассчитывает доходность дивидендов в процентах.

    Формула: (дивиденд / цена акции) * 100

    Пример: HEAD — 200 RUB, цена 5000 RUB
    Доходность = (200 / 5000) * 100 = 4%
    """

    if not last_price or last_price == 0:
        return None

    # Конвертируем в float чтобы избежать ошибки decimal.Decimal / float
    return (float(dividend_amount) / float(last_price)) * 100



# ==================================================
# Расчет предыдущего рабочего дня
# ==================================================

def get_previous_business_day(date):
    """
    Возвращает предыдущий рабочий день.
    Суббота (5) и воскресенье (6) не считаются рабочими днями.

    Пример: если дата закрытия реестра понедельник 28.09.2026,
    то предыдущий рабочий день = пятница 25.09.2026
    """

    result = date - timedelta(days=1)

    # Если получили субботу (5) или воскресенье (6), двигаемся назад
    while result.weekday() >= 5:
        result -= timedelta(days=1)

    return result



# ==================================================
# Формирование текста
# ==================================================

def format_dividends(
        dividends
):


    text = (
        "💰 Дивиденды\n\n"
        "Ближайшие выплаты (даты которых еще не наступили):\n\n"
    )



    if not dividends:

        text += (
            "Нет предстоящих выплат\n"
        )

    else:

        for index, item in enumerate(
                dividends,
                start=1
        ):

            # Дата закрытия реестра
            registry_date = item['date']

            # Форматируем дату закрытия реестра
            registry_date_str = registry_date.strftime('%d.%m.%Y')

            # Рассчитываем "Купить До" (предыдущий рабочий день)
            buy_before_date = get_previous_business_day(registry_date)
            buy_before_date_str = buy_before_date.strftime('%d.%m.%Y')

            # Рассчитываем "Выплата До" (дата закрытия реестра + 10 дней)
            payment_date = registry_date + timedelta(days=10)
            payment_date_str = payment_date.strftime('%d.%m.%Y')

            # Форматируем сумму
            amount_str = format_amount(item['dividend_amount'])

            # Валюта
            currency = item.get('currency', 'RUB')

            # Основная строка
            text += (

                f"{index}. {item['ticker']} — {amount_str} {currency}\n"
                f"   🛒 Купить До: {buy_before_date_str}\n"
                f"   📋 Закрытия реестра: {registry_date_str}\n"
                f"   💵 Выплата До: {payment_date_str}\n"

            )

            # ==================================================
            # Доходность
            # ==================================================

            last_price = item.get('last_price')

            if last_price:

                dividend_yield = calculate_yield(
                    item['dividend_amount'],
                    last_price
                )

                if dividend_yield is not None:

                    yield_str = format_amount(dividend_yield)

                    text += f"   📈 Доходность: {yield_str}%\n"

                else:

                    text += "   📈 Доходность: Н/Д\n"

            else:

                text += "   📈 Доходность: Н/Д\n"


            text += "\n"



    text += (

        "Выберите действие:"

    )


    return text