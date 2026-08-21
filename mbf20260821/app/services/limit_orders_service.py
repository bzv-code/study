from app.database.limit_orders_postgresql import (
    LimitOrdersRepository
)



class LimitOrdersService:


    def __init__(self):

        self.repository = LimitOrdersRepository()



    # =====================================
    # СОЗДАТЬ ЗАЯВКУ
    # =====================================

    async def create_order(

            self,

            user_id: int,

            ticker: str,

            quantity: float,

            limit_price: float,

            buy_price: float

    ):


        return self.repository.add_order(

            user_id=user_id,

            ticker=ticker.upper(),

            quantity=quantity,

            limit_price=limit_price,

            buy_price=buy_price

        )



    # =====================================
    # АКТИВНЫЕ ЗАЯВКИ ПОЛЬЗОВАТЕЛЯ
    # =====================================

    async def get_active_orders(

            self,

            user_id: int

    ) -> list[dict]:


        orders = self.repository.get_active_orders(

            user_id

        )


        return [

            {

                "id": order.id,

                "ticker": order.ticker,

                "quantity": order.quantity,

                "limit_price": order.limit_price,

                "buy_price": order.buy_price,

                "created_at": order.created_at

            }

            for order in orders

        ]



    # =====================================
    # ВСЕ АКТИВНЫЕ ЗАЯВКИ (для монитора)
    # =====================================

    async def get_all_active_orders(self):


        return self.repository.get_all_active_orders()



    # =====================================
    # УДАЛИТЬ ЗАЯВКУ
    # =====================================

    async def delete_order(

            self,

            user_id: int,

            order_id: int

    ) -> bool:


        return self.repository.delete_order(

            user_id=user_id,

            order_id=order_id

        )