import asyncio


from app.bot.client import bot

from app.config import settings

from app.services.alert_service import (
    AlertService
)

from app.services.ticker_service import (
    TickerService
)


print(
    "ALERT PRICE MONITOR LOADED"
)


class AlertMonitorService:


    def __init__(self):

        self.price_alert_service = AlertService()

        self.ticker_service = TickerService()



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

                await self.check_alerts()


            except Exception as e:

                print(
                    "ALERT MONITOR ERROR:",
                    e
                )


            await asyncio.sleep(
                settings.price_alert_check_interval
            )



    # ==================================================
    # CHECK ALERTS
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



        # ==================================================
        # ГРУППИРОВКА ТИКЕТОВ
        # Один запрос = один тикер
        # ==================================================

        tickers = sorted({

            alert.ticker

            for alert in alerts

        })


        print(
            "CHECK TICKERS:",
            tickers
        )


        prices = {}



        # ==================================================
        # ЗАГРУЗКА КОТИРОВОК
        # ==================================================

        for ticker in tickers:


            try:


                quote = await (
                    self.ticker_service
                    .get_quote(ticker)
                )


                if quote:

                    prices[ticker] = float(
                        quote["price"]
                    )


            except Exception as e:


                print(
                    f"QUOTE ERROR {ticker}:",
                    e
                )



        triggered_count = 0

        delete_ids = []



        # ==================================================
        # ПРОВЕРКА УСЛОВИЙ
        # ==================================================

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



        # ==================================================
        # УДАЛЕНИЕ СРАБОТАВШИХ
        # ==================================================

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
    # CONDITION
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
    # SEND MESSAGE
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