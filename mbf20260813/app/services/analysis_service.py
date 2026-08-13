from app.repositories.moex_quotes_repository import MoexQuotesRepository


class AnalysisService:


    def __init__(self):

        self.repository = MoexQuotesRepository()



    async def analyze(
            self,
            ticker: str,
            limit: int = 30
    ):


        history = self.repository.get_history(
            ticker=ticker,
            limit=limit
        )


        if not history:

            return None



        # ClickHouse DESC
        # первая запись = последняя цена

        last = history[0]

        first = history[-1]



        current_price = last["close"]

        start_price = first["close"]



        change_percent = (

            (current_price - start_price)

            /

            start_price

            *

            100

        )



        prices = [

            row["close"]

            for row in history

        ]



        volumes = [

            row["volume"]

            for row in history

        ]



        maximum = max(
            prices
        )


        minimum = min(
            prices
        )



        average_volume = (

            sum(volumes)

            /

            len(volumes)

        )



        # -----------------------------
        # Определение тренда
        # -----------------------------


        if current_price > start_price:

            trend = "🟢 Восходящий"


        elif current_price < start_price:

            trend = "🔴 Нисходящий"


        else:

            trend = "🟡 Боковой"



        return {


            "ticker": ticker,


            "period": limit,


            "current_price": current_price,


            "start_price": start_price,


            "change_percent": change_percent,


            "maximum": maximum,


            "minimum": minimum,


            "average_volume": average_volume,


            "trend": trend

        }