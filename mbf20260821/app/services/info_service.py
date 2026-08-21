from app.repositories.moex_quotes_repository import (
    MoexQuotesRepository
)


print(
    "INFO SERVICE LOADED"
)


class InfoService:


    def __init__(self):

        self.repository = MoexQuotesRepository()



    # ==================================================
    # СПИСОК АКЦИЙ
    # ==================================================

    async def get_stocks_text(self):


        stocks = self.repository.get_year_stocks()



        if not stocks:

            return "📂 Нет данных по акциям"



        text = (

            "📈 Акции (с начала года)\n\n"

        )



        for item in stocks:


            text += (

                f"{item['ticker']} - {item['name']}\n"

            )



        return text



    # ==================================================
    # СПИСОК СЕКТОРОВ
    # ==================================================

    async def get_sectors_text(self):


        rows = self.repository.get_year_sectors()



        if not rows:

            return "📂 Нет данных по секторам"



        # =====================================
        # Группировка по секторам
        # =====================================

        sectors = {}


        for row in rows:


            sector = row["sector"]


            if sector not in sectors:

                sectors[sector] = []


            sectors[sector].append(row)

        text = (

            "🗂 Акции и сектора\n\n"

        )



        for sector, items in sectors.items():


            text += (

                f"📌 {sector}\n"

            )


            for item in items:


                text += (

                    f"{item['ticker']} - {item['name']}\n"

                )


            text += "\n"



        return text