from collections import defaultdict
from statistics import mean


from app.repositories.moex_quotes_repository import (
    MoexQuotesRepository
)


print(
    "ANALYSIS SECTORS SERVICE LOADED"
)


class AnalysisSectorsService:


    def __init__(self):

        self.repository = MoexQuotesRepository()



    # ==================================================
    # АНАЛИЗ СЕКТОРОВ
    # ==================================================

    async def analyze_sectors(

            self,

            period: int = 7

    ):


        print(
            "SECTORS ANALYSIS PERIOD:",
            period
        )



        quotes = self.repository.get_market_history(

            limit=period

        )



        if not quotes:

            return {

                "period": period,

                "sectors_growth": [],

                "sectors_fall": []

            }



        # ==================================================
        # Группируем:
        #
        # sector -> date -> prices
        #
        # ==================================================

        sectors = defaultdict(
            lambda: defaultdict(list)
        )



        for row in quotes:


            sector = row.get(
                "sector"
            )


            date = row.get(
                "date"
            )


            close = row.get(
                "close"
            )


            if not sector or not date or close is None:

                continue



            try:

                price = float(close)

            except ValueError:

                continue



            sectors[sector][date].append(

                price

            )



        result = []



        # ==================================================
        # Расчет средней цены сектора
        # ==================================================

        for sector, days in sectors.items():


            if len(days) < 2:

                continue



            daily_prices = []



            for date, prices in sorted(days.items()):


                daily_prices.append(

                    {

                        "date": date,

                        "price": mean(prices)

                    }

                )



            start = daily_prices[0]["price"]


            end = daily_prices[-1]["price"]



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

                    "sector": sector,

                    "change_percent": round(

                        change,

                        2

                    )

                }

            )



        sectors_growth = sorted(

            result,

            key=lambda x: x["change_percent"],

            reverse=True

        )[:5]



        sectors_fall = sorted(

            [

                item

                for item in result

                if item["change_percent"] < 0

            ],

            key=lambda x: x["change_percent"]

        )[:5]



        response = {


            "period": period,


            "sectors_growth": sectors_growth,


            "sectors_fall": sectors_fall


        }



        print(

            "SECTORS ANALYSIS RESULT:",

            response

        )



        return response