from app.repositories.moex_quotes_repository import (
    MoexQuotesRepository
)


print(
    "ANALYSIS TICKER SERVICE LOADED"
)


class AnalysisTickerService:

    def __init__(self):

        self.repository = MoexQuotesRepository()

    # ==================================================
    # АНАЛИЗ ОДНОЙ АКЦИИ
    # ==================================================

    async def analyze(
            self,
            ticker: str,
            period: int = 7
    ):

        print(
            "TICKER ANALYSIS:",
            ticker,
            period
        )

        quotes = self.repository.get_history(
            ticker=ticker,
            limit=period
        )

        if not quotes:

            print("NO TICKER DATA")
            return None

        clean_quotes = []

        for item in quotes:

            try:

                high = float(item["high"])
                low = float(item["low"])

            except (
                TypeError,
                ValueError,
                KeyError
            ):
                continue

            clean_quotes.append({

                "date": item.get("date"),

                "high": high,

                "low": low

            })

        if not clean_quotes:

            return None

        # ============================================
        # Сортировка по дате
        # ============================================

        clean_quotes.sort(
            key=lambda x: x["date"]
        )

        # ============================================
        # Анализ за 1 день
        # ============================================

        if period == 1:

            day = clean_quotes[-1]

            maximum = day["high"]
            minimum = day["low"]

        # ============================================
        # Анализ за период
        # ============================================

        else:

            maximum = max(
                x["high"]
                for x in clean_quotes
            )

            minimum = min(
                x["low"]
                for x in clean_quotes
            )

        if maximum == 0:

            return None

        # ============================================
        # Волатильность периода
        # ============================================

        change = abs(
            (minimum - maximum)
            / maximum
            * 100
        )

        result = {

            "ticker": ticker,

            "period": period,

            # Оставляем для совместимости с formatter
            "start_price": maximum,
            "current_price": minimum,

            "change_percent": change,

            "maximum": maximum,
            "minimum": minimum

        }

        print(
            "TICKER ANALYSIS RESULT:",
            result
        )

        return result