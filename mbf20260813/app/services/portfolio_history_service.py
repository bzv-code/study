from datetime import date

from app.database.portfolio_history_postgresql import (
    PortfolioHistoryRepository
)


# =====================================
# Максимальное количество сделок в истории
# =====================================

MAX_HISTORY = 10



class PortfolioHistoryService:


    def __init__(self):

        self.repository = PortfolioHistoryRepository()



    # =====================================
    # ДОБАВИТЬ ПРОДАЖУ В ИСТОРИЮ
    # =====================================

    async def add_sell_history(

            self,

            user_id: int,

            ticker: str,

            quantity: float,

            buy_price: float,

            sell_price: float

    ):


        # ==============================
        # Проверка данных
        # ==============================

        if quantity <= 0:

            return None


        if buy_price <= 0 or sell_price <= 0:

            return None



        # ==============================
        # Проверка лимита истории
        # ==============================

        if not await self.can_add_history(

                user_id

        ):

            print(

                f"HISTORY LIMIT REACHED USER={user_id}"

            )

            return None



        # ==============================
        # Расчет сделки
        # ==============================

        buy_total = (

            quantity *

            buy_price

        )


        sell_total = (

            quantity *

            sell_price

        )


        profit = (

            sell_total -

            buy_total

        )


        percent = (

            profit /

            buy_total *

            100

        ) if buy_total else 0



        # ==============================
        # Сохранение истории
        # ==============================

        return self.repository.add_history(

            user_id=user_id,

            ticker=ticker.upper(),

            quantity=quantity,

            buy_price=buy_price,

            sell_price=sell_price,

            buy_total=buy_total,

            sell_total=sell_total,

            profit=profit,

            percent=percent,

            sell_date=date.today()

        )





    # =====================================
    # ПОЛУЧИТЬ ИСТОРИЮ ПОЛЬЗОВАТЕЛЯ
    # =====================================

    async def get_history(

            self,

            user_id: int

    ):


        return self.repository.get_user_history(

            user_id=user_id

        )





    # =====================================
    # ПОЛУЧИТЬ ИСТОРИЮ ПО ТИКЕРУ
    # =====================================

    async def get_ticker_history(

            self,

            user_id: int,

            ticker: str

    ):


        return self.repository.get_history_by_ticker(

            user_id=user_id,

            ticker=ticker.upper()

        )





    # =====================================
    # СТАТИСТИКА ИСТОРИИ
    # =====================================

    async def get_statistics(

            self,

            user_id: int

    ):


        history = await self.get_history(

            user_id

        )


        if not history:

            return {

                "trades": 0,

                "profit": 0,

                "loss": 0,

                "total": 0,

                "win_trades": 0,

                "loss_trades": 0

            }



        total_profit = 0

        total_loss = 0

        win_trades = 0

        loss_trades = 0



        for item in history:


            if item.profit >= 0:

                total_profit += item.profit

                win_trades += 1


            else:

                total_loss += item.profit

                loss_trades += 1



        return {


            "trades": len(history),


            "profit": total_profit,


            "loss": total_loss,


            "total": total_profit + total_loss,


            "win_trades": win_trades,


            "loss_trades": loss_trades

        }





    # =====================================
    # ОЧИСТИТЬ ИСТОРИЮ
    # =====================================

    async def clear_history(

            self,

            user_id: int

    ):


        return self.repository.clear_history(

            user_id=user_id

        )





    # =====================================
    # ПРОВЕРКА ЛИМИТА ИСТОРИИ
    # =====================================

    async def can_add_history(

            self,

            user_id: int

    ) -> bool:


        history_count = self.repository.count_history(

            user_id=user_id

        )


        print(

            f"HISTORY COUNT USER={user_id}: {history_count}/{MAX_HISTORY}"

        )


        return history_count < MAX_HISTORY





    # =====================================
    # ТЕКУЩИЙ ЛИМИТ ИСТОРИИ
    # =====================================

    def get_history_limit(

            self

    ) -> int:


        return MAX_HISTORY