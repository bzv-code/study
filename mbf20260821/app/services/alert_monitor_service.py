import asyncio


from app.bot.client import bot

from app.config import settings

from app.services.alert_service import (
    AlertService
)

from app.services.portfolio_service import (
    PortfolioService
)

from app.services.portfolio_history_service import (
    PortfolioHistoryService
)

from app.services.limit_orders_service import (
    LimitOrdersService
)

from app.repositories.moex_quotes_repository import (
    MoexQuotesRepository
)

from app.utils.portfolio_formatter import (
    PortfolioFormatter
)

from app.utils.trading_hours import (
    is_alert_check_allowed,
    now_msk
)

from app.keyboards.general_menu import (
    main_menu
)


print(
    "ALERT PRICE MONITOR LOADED"
)


class AlertMonitorService:


    def __init__(self):

        self.price_alert_service = AlertService()

        self.portfolio_service = PortfolioService()

        self.portfolio_history_service = PortfolioHistoryService()

        self.limit_orders_service = LimitOrdersService()

        self.repository = MoexQuotesRepository()



    # ==================================================
    # START MONITOR
    # ==================================================

    async def run(self):

        print(
            "ALERT PRICE MONITOR STARTED"
        )


        print(
            "CHECK INTERVAL:",
            settings.price_alert_check_interval,
            "seconds"
        )


        while True:


            try:


                # =====================================
                # Тихие часы: 00:10–05:50 МСК
                # =====================================

                if is_alert_check_allowed():


                    await self.check_alerts()


                    await self.check_limit_orders()


                else:


                    print(

                        "ALERT MONITOR: 00:10-05:50 MSK, SKIP CHECK |",

                        "NOW MSK:",

                        now_msk().strftime("%d.%m.%Y %H:%M")

                    )


            except Exception as e:

                print(
                    "ALERT MONITOR ERROR:",
                    e
                )


            await asyncio.sleep(

                settings.price_alert_check_interval

            )



    # ==================================================
    # CHECK ALERTS (уведомления)
    # ==================================================

    async def check_alerts(self):


        alerts = (
            self.price_alert_service
            .get_active_alerts()
        )


        print(
            "ACTIVE ALERTS:",
            len(alerts)
        )


        if not alerts:

            return



        tickers = sorted({

            alert.ticker

            for alert in alerts

        })


        print(
            "CHECK TICKERS:",
            tickers
        )


        prices = {}



        for ticker in tickers:


            try:


                quote = self.repository.get_last_quote_m10(

                    ticker

                )


                if quote:


                    prices[ticker] = float(

                        quote["close"]

                    )


            except Exception as e:


                print(

                    f"QUOTE ERROR {ticker}:",

                    e

                )



        triggered_count = 0

        delete_ids = []



        for alert in alerts:


            current_price = prices.get(

                alert.ticker

            )


            if current_price is None:

                continue



            if not self.is_triggered(

                alert,

                current_price

            ):

                continue



            sent = await self.send_alert(

                user_id=alert.user_id,

                ticker=alert.ticker,

                current_price=current_price,

                target_price=alert.target_price,

                condition=alert.condition

            )


            if sent:


                delete_ids.append(

                    alert.id

                )


                triggered_count += 1



        for alert_id in delete_ids:


            result = (
                self.price_alert_service
                .delete_alert(alert_id)
            )


            print(
                "ALERT DELETE:",
                alert_id,
                result
            )



        print(
            "MONITOR RESULT:",
            {
                "alerts": len(alerts),
                "tickers": len(tickers),
                "triggered": triggered_count
            }
        )



    # ==================================================
    # CHECK LIMIT ORDERS (лимитные заявки)
    # ==================================================

    async def check_limit_orders(self):


        orders = await (
            self.limit_orders_service
            .get_all_active_orders()
        )


        if not orders:

            return



        print(
            "ACTIVE LIMIT ORDERS:",
            len(orders)
        )



        # =====================================
        # Максимумы за последние 10 баров m10
        # =====================================

        tickers = sorted({

            order.ticker

            for order in orders

        })


        highs = {}


        for ticker in tickers:


            try:


                bars = self.repository.get_recent_bars_m10(

                    ticker,

                    limit=10

                )


                if bars:


                    highs[ticker] = max(bars)


            except Exception as e:


                print(

                    f"LIMIT ORDER QUOTE ERROR {ticker}:",

                    e

                )



        for order in orders:


            max_high = highs.get(

                order.ticker

            )


            if max_high is None:

                continue



            # цена не достигла уровня заявки

            if max_high < order.limit_price:

                continue



            # =====================================
            # ИСПОЛНЕНИЕ ЗАЯВКИ
            # =====================================

            await self.execute_limit_order(

                order

            )



    # ==================================================
    # EXECUTE LIMIT ORDER
    # ==================================================

    async def execute_limit_order(

            self,

            order

    ):


        user_id = order.user_id

        ticker = order.ticker

        quantity = order.quantity

        sell_price = order.limit_price



        print(

            "EXECUTING LIMIT ORDER:",

            order.id,

            ticker

        )



        # =====================================
        # Проверяем позицию в портфеле
        # =====================================

        portfolio = await self.portfolio_service.get_portfolio(

            user_id=user_id

        )


        position = next(

            (

                item

                for item in portfolio

                if item["ticker"] == ticker

            ),

            None

        )



        # акций не хватает — отменяем заявку

        if (

            position is None

            or position["quantity"] < quantity

        ):


            await self.limit_orders_service.delete_order(

                user_id=user_id,

                order_id=order.id

            )


            await bot.send_message(

                user_id=user_id,

                text=(

                    "❌ Лимитная заявка отменена\n\n"

                    f"📈 {ticker}\n\n"

                    "В портфеле недостаточно акций\n"

                    "для исполнения заявки"

                )

            )


            return



        # =====================================
        # Проверяем лимит истории
        # =====================================

        can_sell = await (
            self.portfolio_history_service
            .can_add_history(user_id)
        )


        if not can_sell:


            print(

                "LIMIT ORDER SKIP: HISTORY FULL",

                order.id

            )


            return



        buy_price = position["buy_price"]



        # =====================================
        # Сохраняем историю сделки
        # =====================================

        history_result = await (
            self.portfolio_history_service
            .add_sell_history(

                user_id=user_id,

                ticker=ticker,

                quantity=quantity,

                buy_price=buy_price,

                sell_price=sell_price

            )
        )


        if history_result is None:


            print(

                "LIMIT ORDER HISTORY ERROR:",

                order.id

            )


            return



        # =====================================
        # Уменьшаем позицию
        # =====================================

        sell_result = await self.portfolio_service.sell_position(

            user_id=user_id,

            ticker=ticker,

            quantity=quantity

        )


        if not sell_result:


            print(

                "LIMIT ORDER SELL ERROR:",

                order.id

            )


            return



        # =====================================
        # Удаляем исполненную заявку
        # =====================================

        await self.limit_orders_service.delete_order(

            user_id=user_id,

            order_id=order.id

        )



        # =====================================
        # Расчет результата
        # =====================================

        buy_total = quantity * buy_price

        sell_total = quantity * sell_price

        profit = sell_total - buy_total

        percent = (

            profit /

            buy_total *

            100

        ) if buy_total else 0



        # =====================================
        # Сообщение об исполнении
        # =====================================

        await bot.send_message(

            user_id=user_id,

            text=(

                "✅ Акция продана\n\n"

                f"📈 {ticker}\n\n"

                f"Количество:\n{quantity:.2f} шт.\n\n"

                f"💰 Покупка:\n{buy_price:.2f} ₽\n\n"

                f"💵 Продажа:\n{sell_price:.2f} ₽\n\n"

                f"Результат:\n{profit:+.2f} ₽\n\n"

                f"Доходность:\n{percent:+.2f}%\n\n"

                "📂 История сделки сохранена"

            )

        )



        # =====================================
        # Обновленный портфель
        # =====================================

        portfolio = await self.portfolio_service.get_portfolio(

            user_id=user_id

        )


        portfolio_message = await PortfolioFormatter.format_portfolio(

            portfolio,

            user_id

        )


        await bot.send_message(

            user_id=user_id,

            text=portfolio_message

        )



        # =====================================
        # Главное меню
        # =====================================

        await bot.send_message(

            user_id=user_id,

            text="Выберите действие:",

            attachments=[

                main_menu()

            ]

        )



        print(

            "LIMIT ORDER EXECUTED:",

            order.id

        )



    # ==================================================
    # CONDITION (уведомления)
    # ==================================================

    def is_triggered(

            self,

            alert,

            current_price: float

    ) -> bool:


        if alert.condition == "above":

            return (

                current_price >= alert.target_price

            )



        if alert.condition == "below":

            return (

                current_price <= alert.target_price

            )


        return False



    # ==================================================
    # SEND MESSAGE (уведомления)
    # ==================================================

    async def send_alert(

            self,

            user_id: int,

            ticker: str,

            current_price: float,

            target_price: float,

            condition: str

    ) -> bool:


        direction = (

            "выше"

            if condition == "above"

            else "ниже"

        )


        text = (

            "🔔 Сработало уведомление\n\n"

            f"📈 {ticker}\n\n"

            f"Цена стала {direction} уровня\n\n"

            f"Текущая цена: {current_price:.2f} ₽\n"

            f"Ваш уровень: {target_price:.2f} ₽"

        )


        try:


            await bot.send_message(

                user_id=user_id,

                text=text

            )


            print(

                "ALERT SENT:",

                ticker,

                user_id

            )


            return True



        except Exception as e:


            print(

                "SEND ALERT ERROR:",

                ticker,

                user_id,

                e

            )


            return False