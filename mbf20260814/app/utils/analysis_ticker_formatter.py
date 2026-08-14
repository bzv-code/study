print(
    "ANALYSIS TICKER FORMATTER LOADED"
)


class AnalysisTickerFormatter:

    @classmethod
    def format(

            cls,

            result: dict

    ) -> str:

        if not result:

            return (
                "❌ Нет данных анализа"
            )

        ticker = result.get(
            "ticker",
            "-"
        )

        period = result.get(
            "period",
            7
        )

        change = result.get(
            "change_percent",
            0
        )

        maximum = result.get(
            "maximum",
            0
        )

        minimum = result.get(
            "minimum",
            0
        )

        text = (

            f"📉 Анализ {ticker}\n\n"

            f"📅 Период: {period} дней\n\n"

            f"📈 Изменение: {change:.2f}%\n\n"

            "💰 Цена\n"

            f"⬆ Максимум: {maximum:.2f} ₽\n"

            f"⬇ Минимум: {minimum:.2f} ₽"

        )

        return text