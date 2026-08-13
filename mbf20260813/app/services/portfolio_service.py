from datetime import date

from app.database.portfolio_postgresql import PortfolioRepository
from app.services.ticker_service import TickerService


class PortfolioService:


    def __init__(self):

        self.repository = PortfolioRepository()

        self.ticker_service = TickerService()



    # =====================================
    # ПОЛУЧИТЬ ПОРТФЕЛЬ
    # =====================================

    async def get_portfolio(
            self,
            user_id: int
    ) -> list[dict]:

        positions = self.repository.get_user_portfolio(
            user_id
        )

        if not positions:
            return []

        portfolio = {}

        for position in positions:

            quote = await self.ticker_service.get_quote(
                position.ticker
            )

            if not quote:
                continue

            ticker = position.ticker

            if ticker not in portfolio:
                portfolio[ticker] = {

                    "ticker": ticker,

                    "quantity": 0,

                    "invested": 0,

                    "current_price": quote["price"]

                }

            portfolio[ticker]["quantity"] += position.quantity

            portfolio[ticker]["invested"] += (
                    position.quantity *
                    position.buy_price
            )

        result = []

        for item in portfolio.values():
            quantity = item["quantity"]

            invested = item["invested"]

            current_price = item["current_price"]

            buy_price = invested / quantity

            current_value = (
                    quantity *
                    current_price
            )

            profit = (
                    current_value -
                    invested
            )

            percent = (
                    profit /
                    invested *
                    100
            ) if invested else 0

            result.append(

                {

                    "ticker": item["ticker"],

                    "quantity": quantity,

                    "buy_price": buy_price,

                    "current_price": current_price,

                    "invested": invested,

                    "current_value": current_value,

                    "profit": profit,

                    "percent": percent,

                }

            )

        result.sort(
            key=lambda x: x["ticker"]
        )

        return result




    # =====================================
    # ДОБАВИТЬ АКЦИЮ В ПОРТФЕЛЬ
    # =====================================

    async def add_position(

            self,

            user_id: int,

            ticker: str,

            quantity: float,

            buy_price: float

    ):

        return self.repository.add_position(

            user_id=user_id,

            ticker=ticker.upper(),

            quantity=quantity,

            buy_price=buy_price,

            buy_date=date.today()

        )




    # =====================================
    # УДАЛИТЬ ПО ID
    # =====================================

    async def delete_position(

            self,

            position_id: int

    ) -> bool:

        return self.repository.delete_position(

            position_id=position_id

        )




    # =====================================
    # УДАЛИТЬ ПО ТИКЕРУ
    # =====================================

    async def delete_by_ticker(

            self,

            user_id: int,

            ticker: str

    ) -> bool:

        return self.repository.delete_by_ticker(

            user_id=user_id,

            ticker=ticker.upper()

        )

    # =====================================
    # ПРОДАТЬ ЧАСТЬ ПОЗИЦИИ
    # =====================================

    async def sell_position(

            self,

            user_id: int,

            ticker: str,

            quantity: float

    ) -> bool:


        result = self.repository.reduce_position(

            user_id=user_id,

            ticker=ticker.upper(),

            quantity=quantity

        )


        if result is None:

            return False


        return True