from app.repositories.moex_quotes_repository import MoexQuotesRepository


class TickerService:


    def __init__(self):

        self.repository = MoexQuotesRepository()



    async def get_quote(
            self,
            ticker: str
    ):

        quote = self.repository.get_last_quote(
            ticker
        )


        if not quote:
            return None


        return {

            "ticker": quote["ticker"],
            "name": quote["name"],
            "price": quote["close"],
            "date": quote["date"],
            "sector": quote["sector"]

        }



    async def get_history(
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


        return history