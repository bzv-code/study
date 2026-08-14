from maxapi import Router

from maxapi.types import MessageCallback
from maxapi.context.base import BaseContext

from app.payloads.callback_payloads import (
    AnalysisPeriodPayload
)

from app.services.analysis_ticker_service import (
    AnalysisTickerService
)

from app.utils.analysis_ticker_formatter import (
    AnalysisTickerFormatter
)

from app.keyboards.analysis_ticker_period_menu import (
    analysis_ticker_period_menu
)


print(
    "ANALYSIS TICKER PERIOD CALLBACK LOADED"
)


router = Router()

service = AnalysisTickerService()


# ==================================================
# АНАЛИЗ ТИКЕТА ПО ПЕРИОДУ
# ==================================================

@router.message_callback(
    AnalysisPeriodPayload.filter()
)
async def analysis_ticker_period_callback(
        event: MessageCallback,
        context: BaseContext
):

    print("=" * 50)
    print(
        "ANALYSIS TICKER PERIOD CALLBACK"
    )
    print(
        "PAYLOAD:",
        event.callback.payload
    )
    print("=" * 50)

    await event.answer()

    # ==================================================
    # Получаем тикер
    # ==================================================

    data = await context.get_data()

    print(
        "CONTEXT:",
        data
    )

    ticker = data.get(
        "analysis_ticker"
    )

    if not ticker:

        await event.message.answer(
            "❌ Тикер анализа не найден"
        )

        return

    # ==================================================
    # Получаем период
    # ==================================================

    payload = event.callback.payload

    if "|" not in payload:

        await event.message.answer(
            "❌ Ошибка выбора периода"
        )

        return

    _, period_value = payload.split(
        "|",
        1
    )

    try:

        period = int(period_value)

    except ValueError:

        await event.message.answer(
            "❌ Некорректный период"
        )

        return

    print(
        "TICKER ANALYSIS PERIOD:",
        period
    )

    # ==================================================
    # Запуск анализа
    # ==================================================

    result = await service.analyze(
        ticker=ticker,
        period=period
    )

    print(
        "TICKER ANALYSIS RESULT:",
        result
    )

    if not result:

        await event.message.answer(
            f"❌ Нет данных по акции {ticker}"
        )

        return

    # ==================================================
    # Добавляем период
    # ==================================================

    result["period"] = period

    # ==================================================
    # Форматирование
    # ==================================================

    text = AnalysisTickerFormatter.format(
        result
    )

    # ==================================================
    # Ответ
    # ==================================================

    await event.message.answer(
        text,
        attachments=[
            analysis_ticker_period_menu()
        ]
    )

    print(
        "TICKER ANALYSIS SENT"
    )

    # ==================================================
    # НЕ очищаем context.
    # analysis_ticker должен сохраниться,
    # чтобы пользователь мог переключать периоды
    # без повторного ввода тикера.
    # ==================================================