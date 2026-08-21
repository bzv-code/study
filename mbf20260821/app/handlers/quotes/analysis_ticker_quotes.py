from maxapi import Router

from maxapi.types import MessageCreated
from maxapi.context.base import BaseContext


from app.states.user import UserStates


from app.repositories.moex_quotes_repository import (
    MoexQuotesRepository
)


from app.utils.analysis_ticker_formatter import (
    AnalysisTickerFormatter
)


from app.keyboards.analysis_ticker_period_menu import (
    analysis_ticker_period_menu
)


from app.services.analysis_ticker_chart_attachment_service import (
    AnalysisTickerChartAttachmentService
)


chart_attachment_service = AnalysisTickerChartAttachmentService()


print(
    "ANALYSIS TICKER QUOTES LOADED"
)



router = Router()


repository = MoexQuotesRepository()



# ==================================================
# НОРМАЛИЗАЦИЯ ТИКЕРА
# ==================================================

def normalize_ticker(raw: str) -> str:
    """
    Приводит тикер к единому виду (верхний регистр, без пробелов):

    GAZP -> GAZP
    Gazp -> GAZP
    gazp -> GAZP
    "  gazp  " -> GAZP
    """

    return raw.strip().upper()



# ==================================================
# ВВОД ТИКЕРА ДЛЯ АНАЛИЗА
# ==================================================

@router.message_created(

    UserStates.WAIT_ANALYSIS_TICKER

)

async def analysis_ticker_quotes_handler(

        event: MessageCreated,

        context: BaseContext

):


    text = getattr(

        event.message.body,

        "text",

        None

    )


    if not text:


        await event.message.answer(

            "❌ Не удалось определить тикер"

        )

        return



    # =====================================
    # Приводим к единому регистру
    # =====================================

    ticker = normalize_ticker(text)



    print(

        "ANALYSIS TICKER INPUT:",

        ticker

    )



    try:


        # =====================================
        # Сохраняем тикер для дальнейшего выбора периода
        # =====================================

        await context.update_data(

            analysis_ticker=ticker

        )



        # =====================================
        # Берем последние 2 торговых дня
        # =====================================

        quotes = repository.get_history(

            ticker=ticker,

            limit=2

        )



        if not quotes or len(quotes) < 2:


            await event.message.answer(

                f"❌ Нет данных по акции {ticker}"

            )


            await context.clear()

            return



        # =====================================
        # Сортировка от старых к новым
        # =====================================

        quotes.sort(

            key=lambda x: x["date"]

        )



        previous_day = quotes[-2]

        last_day = quotes[-1]



        start_price = float(

            previous_day["close"]

        )


        current_price = float(

            last_day["close"]

        )



        # =====================================
        # Изменение цены закрытия день-ко-дню
        # =====================================

        change = (

            (current_price - start_price)

            /

            start_price

            *

            100

        )



        result = {


            "ticker": ticker,


            "period": 1,


            "start_price": start_price,


            "current_price": current_price,


            "change_percent": change,


            "maximum": float(

                last_day.get(

                    "high",

                    current_price

                )

            ),


            "minimum": float(

                last_day.get(

                    "low",

                    current_price

                )

            )

        }



        print(

            "TICKER ANALYSIS RESULT:",

            result

        )



        message = AnalysisTickerFormatter.format(

            result

        )



        # =====================================
        # График за период 1 день
        # =====================================

        chart_attachment = await chart_attachment_service.get_chart_attachment(

            ticker=ticker,

            limit=1

        )



        # =====================================
        # Собираем вложения:
        # график + кнопки периода
        # =====================================

        attachments = []


        if chart_attachment:

            attachments.append(

                chart_attachment

            )


        attachments.append(

            analysis_ticker_period_menu()

        )



        # =====================================
        # Текст + график + кнопки в ОДНОМ сообщении
        # =====================================

        await event.message.answer(

            message,

            attachments=attachments

        )



        # ВАЖНО:
        # context НЕ очищаем
        # ticker нужен для кнопок 7/14/30 дней


        await context.set_state(

            UserStates.WAIT_ANALYSIS_TICKER_PERIOD

        )



        print(

            "STATE -> WAIT_ANALYSIS_TICKER_PERIOD"

        )



    except Exception as e:


        print(

            "ANALYSIS TICKER ERROR:",

            e

        )


        await event.message.answer(

            "❌ Ошибка анализа тикета"

        )


        await context.clear()