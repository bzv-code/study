from app.services.portfolio_history_service import (
    PortfolioHistoryService
)


class PortfolioFormatter:


    history_service = PortfolioHistoryService()



    # =====================================
    # ФОРМАТ ПОРТФЕЛЯ
    # =====================================

    @classmethod
    async def format_portfolio(

            cls,

            portfolio: list[dict],

            user_id: int

    ) -> str:



        # =====================================
        # ПУСТОЙ ПОРТФЕЛЬ
        # =====================================

        if not portfolio:


            statistics = await cls.history_service.get_statistics(

                user_id

            )


            return (

                "📂 Портфель пуст\n\n"


                "📜 История сделок\n\n"

                f"Сделок: {statistics['trades']} / 10\n\n"

                f"✅ Прибыльных: {statistics['win_trades']}\n"

                f"❌ Убыточных: {statistics['loss_trades']}\n\n"

                f"💰 Прибыль: {statistics['total']:+.2f} ₽"

            )



        text = (

            "📊 Мой портфель\n\n"

        )



        total_invested = 0

        total_value = 0



        for item in portfolio:


            ticker = item["ticker"]

            quantity = item["quantity"]

            buy_price = item["buy_price"]

            current_price = item["current_price"]

            invested = item["invested"]

            current_value = item["current_value"]

            profit = item["profit"]

            percent = item["percent"]



            total_invested += invested

            total_value += current_value



            emoji = (

                "📈"

                if profit >= 0

                else

                "📉"

            )



            text += (

                f"{emoji} {ticker}\n\n"

                f"Количество: {quantity:.2f} шт.\n"

                f"Средняя цена: {buy_price:.2f} ₽\n"

                f"Текущая цена: {current_price:.2f} ₽\n\n"

                f"💰 Вложено: {invested:.2f} ₽\n"

                f"📦 Стоимость: {current_value:.2f} ₽\n"

                f"Результат: {profit:+.2f} ₽\n"

                f"Доходность: {percent:+.2f}%\n\n"

                "--------------------\n\n"

            )



        total_profit = (

            total_value -

            total_invested

        )



        total_percent = (

            total_profit /

            total_invested *

            100

        ) if total_invested else 0




        text += (

            "📌 ИТОГО\n\n"

            f"💰 Вложено: {total_invested:.2f} ₽\n"

            f"📦 Стоимость: {total_value:.2f} ₽\n"

            f"Результат: {total_profit:+.2f} ₽\n"

            f"Доходность: {total_percent:+.2f}%\n\n"

        )



        # =====================================
        # ИСТОРИЯ СДЕЛОК
        # =====================================


        statistics = await cls.history_service.get_statistics(

            user_id

        )



        text += (

            "📜 История сделок\n\n"

            f"Сделок: {statistics['trades']} / 10\n\n"

            f"✅ Прибыльных: {statistics['win_trades']}\n"

            f"❌ Убыточных: {statistics['loss_trades']}\n\n"

            f"💰 Прибыль: {statistics['total']:+.2f} ₽"

        )



        return text