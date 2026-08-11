from collections import defaultdict


from app.repositories.moex_quotes_repository import (
    MoexQuotesRepository
)



print(
    "ANALYSIS STOCKS SERVICE LOADED"
)



class AnalysisStocksService:


    def __init__(self):

        self.repository = MoexQuotesRepository()



    # ==================================================
    # АНАЛИЗ АКЦИЙ
    # ==================================================

    async def analyze_stocks(

            self,

            period: int = 7

    ):


        print(
            "STOCKS ANALYSIS PERIOD:",
            period
        )



        quotes = self.repository.get_market_history(

            limit=period

        )



        if not quotes:


            return {

                "period": period,

                "stocks_growth": [],

                "stocks_fall": []

            }



        stocks = defaultdict(list)

        info = {}



        # ==================================================
        # Группировка акций
        # ==================================================

        for row in quotes:


            ticker = row.get(
                "ticker"
            )


            close = row.get(
                "close"
            )


            if not ticker or close is None:

                continue



            stocks[ticker].append(

                row

            )



            info[ticker] = {

                "name": row.get(
                    "name"
                ),

                "sector": row.get(
                    "sector"
                )

            }



        result = []



        # ==================================================
        # Расчет изменения
        # ==================================================

        for ticker, items in stocks.items():


            items.sort(

                key=lambda x: x.get(
                    "date"
                )

            )



            if len(items) < 2:

                continue



            try:

                start = float(

                    items[0]["close"]

                )


                end = float(

                    items[-1]["close"]

                )


            except (

                TypeError,

                ValueError

            ):

                continue



            if start == 0:

                continue



            change = (

                (end - start)

                /

                start

                *

                100

            )



            result.append(

                {

                    "ticker": ticker,

                    "name": info[ticker].get(
                        "name"
                    ),

                    "sector": info[ticker].get(
                        "sector"
                    ),

                    "change_percent": change

                }

            )



        # ==================================================
        # Рост
        # ==================================================

        stocks_growth = sorted(

            result,

            key=lambda x: x["change_percent"],

            reverse=True

        )[:5]



        # ==================================================
        # Падение
        # ==================================================

        stocks_fall = sorted(

            [

                x for x in result

                if x["change_percent"] < 0

            ],

            key=lambda x: x["change_percent"]

        )[:5]



        response = {


            "period": period,


            "stocks_growth": stocks_growth,


            "stocks_fall": stocks_fall


        }



        print(

            "STOCKS ANALYSIS RESULT:",

            response

        )



        return response