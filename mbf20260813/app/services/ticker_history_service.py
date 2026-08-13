from app.repositories.moex_quotes_repository import (
    MoexQuotesRepository
)


print(
    "TICKER HISTORY SERVICE LOADED"
)



class TickerHistoryService:


    def __init__(self):

        self.repository = MoexQuotesRepository()



    async def get_history(

            self,

            ticker: str,

            limit: int = 7

    ):


        rows = self.repository.get_history(

            ticker=ticker,

            limit=limit

        )


        if not rows:

            return []



        rows.sort(

            key=lambda x: x["date"],

            reverse=True

        )


        result = []



        for row in rows:


            result.append(

                {

                    "date": row["date"],

                    "close": float(

                        row["close"]

                    ),

                    "high": float(

                        row["high"]

                    ),

                    "low": float(

                        row["low"]

                    )

                }

            )


        return result