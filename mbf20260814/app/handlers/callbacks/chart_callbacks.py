from maxapi import Router
from maxapi.types import MessageCallback
from maxapi.context.base import BaseContext

from app.services.ticker_chart_service import (
    TickerChartService
)

from app.services.ticker_chart_media_service import (
    TickerChartMediaService
)

from app.payloads.callback_payloads import (
    ChartPayload
)


print(
    "CHART CALLBACK LOADED"
)


router = Router()


chart_service = TickerChartService()

chart_media_service = TickerChartMediaService()


# ==================================================
# ГРАФИК АКЦИИ
# ==================================================

@router.message_callback(
    ChartPayload.filter()
)
async def chart_callback(
        event: MessageCallback,
        context: BaseContext
):

    print("=" * 50)
    print("CHART CALLBACK")
    print(
        "PAYLOAD:",
        event.callback.payload
    )
    print("=" * 50)

    await event.answer()

    data = await context.get_data()

    print(
        "CONTEXT:",
        data
    )

    ticker = data.get(
        "ticker"
    )

    if not ticker:

        await event.message.answer(
            "❌ Нет выбранной акции"
        )

        return

    print(
        "CHART TICKER:",
        ticker
    )

    await event.message.answer(
        "📊 Строю график..."
    )

    # =====================================
    # Строим график
    # =====================================

    file_path = await chart_service.create_price_chart(

        ticker=ticker,

        limit=30

    )

    if not file_path:

        await event.message.answer(
            "❌ Нет данных для графика"
        )

        return

    print(
        "CHART FILE:",
        file_path
    )

    # =====================================
    # Загружаем график
    # =====================================

    try:

        media = await chart_media_service.upload_image(
            file_path
        )

        print(
            "MEDIA UPLOADED"
        )

    except Exception as e:

        print(
            f"MEDIA UPLOAD ERROR: {e}"
        )

        await event.message.answer(
            "❌ Не удалось загрузить график."
        )

        return

    # =====================================
    # Отправляем пользователю
    # =====================================

    await event.message.answer(

        f"📊 График {ticker}",

        attachments=[

            media

        ]

    )

    print(
        "CHART SENT"
    )