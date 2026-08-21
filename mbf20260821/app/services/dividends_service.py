from app.repositories.dividends_repository import DividendsRepository
from app.repositories.moex_quotes_repository import MoexQuotesRepository


print(
    "DIVIDENDS SERVICE LOADED"
)


class DividendsService:


    def __init__(self):

        self.repository = DividendsRepository()

        self.quotes_repository = MoexQuotesRepository()



    # ==================================================
    # ПОЛУЧИТЬ БУДУЩИЕ ДИВИДЕНДЫ
    # ==================================================

    async def get_future_dividends(self):


        print(
            "DIVIDENDS SERVICE: get_future_dividends"
        )



        dividends = self.repository.get_future_dividends()



        if not dividends:

            return []



        # ==================================================
        # Для каждого тикера получаем последнюю цену
        # ==================================================

        for item in dividends:

            ticker = item['ticker']

            print(
                "DIVIDENDS SERVICE: get price for",
                ticker
            )


            try:

                quote = self.quotes_repository.get_last_quote(
                    ticker
                )


                if quote:

                    item['last_price'] = quote['close']

                else:

                    item['last_price'] = None


            except Exception as e:

                print(
                    "DIVIDENDS SERVICE ERROR getting price:",
                    e
                )

                item['last_price'] = None



        return dividends