from app.database.alert_postgresql import (
    AlertRepository
)


from app.services.ticker_service import (
    TickerService
)



print(
    "PRICE ALERT SERVICE LOADED"
)



class AlertService:


    def __init__(self):

        self.repository = AlertRepository()

        self.ticker_service = TickerService()



    # ==================================================
    # СОЗДАТЬ УВЕДОМЛЕНИЕ
    # ==================================================

    async def create_alert(

            self,

            user_id: int,

            ticker: str,

            target_price: float,

            condition: str

    ):


        ticker = ticker.upper().strip()

        condition = condition.lower().strip()



        if not ticker:


            return {

                "success": False,

                "message": "Не указан тикер."

            }



        if condition not in (

            "above",

            "below"

        ):


            return {

                "success": False,

                "message": "Некорректное условие уведомления."

            }



        # =====================================
        # Максимум 10 уведомлений
        # =====================================

        count = self.repository.count_active(

            user_id

        )


        if count >= 10:


            return {

                "success": False,

                "message":
                    "Можно создать максимум 10 уведомлений."

            }



        # =====================================
        # Один тикер = одно уведомление
        # =====================================

        if self.repository.exists(

                user_id=user_id,

                ticker=ticker

        ):


            return {

                "success": False,

                "message":
                    f"Для {ticker} уже существует уведомление."

            }



        alert = self.repository.create(

            user_id=user_id,

            ticker=ticker,

            target_price=target_price,

            condition=condition

        )



        return {

            "success": True,

            "alert": alert

        }



    # ==================================================
    # МОИ УВЕДОМЛЕНИЯ
    # ==================================================

    def get_user_alerts(

            self,

            user_id: int

    ):


        return self.repository.get_user_alerts(

            user_id

        )



    # ==================================================
    # АКТИВНЫЕ УВЕДОМЛЕНИЯ
    # Для мониторинга
    # ==================================================

    def get_active_alerts(self):


        return self.repository.get_active()



    # ==================================================
    # ПРОВЕРКА УВЕДОМЛЕНИЙ
    #
    # Один запрос на один тикер
    # ==================================================

    async def check_alerts(self):


        alerts = self.repository.get_active()



        if not alerts:


            return []



        print(

            "ACTIVE ALERTS:",

            len(alerts)

        )



        # =====================================
        # Группировка тикеров
        # =====================================

        tickers = {

            alert.ticker

            for alert in alerts

        }



        print(

            "UNIQUE TICKERS:",

            tickers

        )



        prices = {}



        # =====================================
        # Получаем цены
        # один запрос на тикер
        # =====================================

        for ticker in tickers:


            try:


                quote = await self.ticker_service.get_quote(

                    ticker

                )



                if quote:


                    prices[ticker] = quote["price"]



            except Exception as e:


                print(

                    f"QUOTE ERROR {ticker}:",

                    e

                )



        triggered = []



        # =====================================
        # Проверяем условия
        # =====================================

        for alert in alerts:


            current_price = prices.get(

                alert.ticker

            )


            if current_price is None:


                continue



            if self.is_triggered(

                alert,

                current_price

            ):


                triggered.append(

                    {

                        "id": alert.id,

                        "user_id": alert.user_id,

                        "ticker": alert.ticker,

                        "current_price": current_price,

                        "target_price": alert.target_price,

                        "condition": alert.condition

                    }

                )



        return triggered



    # ==================================================
    # ПРОВЕРКА УСЛОВИЯ
    # ==================================================

    def is_triggered(

            self,

            alert,

            current_price: float

    ) -> bool:


        if alert.condition == "above":


            return current_price >= alert.target_price



        if alert.condition == "below":


            return current_price <= alert.target_price



        return False



    # ==================================================
    # УДАЛИТЬ УВЕДОМЛЕНИЕ
    # ==================================================

    def delete_alert(

            self,

            alert_id: int

    ) -> bool:


        return self.repository.delete(

            alert_id

        )



    # ==================================================
    # ОТКЛЮЧИТЬ УВЕДОМЛЕНИЕ
    # ==================================================

    def deactivate(

            self,

            alert_id: int

    ):


        return self.repository.deactivate(

            alert_id

        )