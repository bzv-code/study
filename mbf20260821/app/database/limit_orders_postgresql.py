from sqlalchemy import select

from app.database.connect_postgresql import SessionLocal
from app.database.models_postgresql import LimitOrder



class LimitOrdersRepository:


    # =====================================
    # СОЗДАТЬ ЗАЯВКУ
    # =====================================

    @staticmethod
    def add_order(

            user_id: int,
            ticker: str,
            quantity: float,
            limit_price: float,
            buy_price: float

    ) -> LimitOrder:


        with SessionLocal() as session:


            order = LimitOrder(

                user_id=user_id,

                ticker=ticker.upper(),

                quantity=quantity,

                limit_price=limit_price,

                buy_price=buy_price

            )


            session.add(order)

            session.commit()

            session.refresh(order)


            return order



    # =====================================
    # АКТИВНЫЕ ЗАЯВКИ ПОЛЬЗОВАТЕЛЯ
    # =====================================

    @staticmethod
    def get_active_orders(

            user_id: int

    ) -> list[LimitOrder]:


        with SessionLocal() as session:


            result = session.scalars(

                select(LimitOrder)

                .where(

                    LimitOrder.user_id == user_id,

                    LimitOrder.is_active == True

                )

                .order_by(

                    LimitOrder.created_at.asc()

                )

            )


            return list(result)



    # =====================================
    # ВСЕ АКТИВНЫЕ ЗАЯВКИ (для монитора)
    # =====================================

    @staticmethod
    def get_all_active_orders() -> list[LimitOrder]:


        with SessionLocal() as session:


            result = session.scalars(

                select(LimitOrder)

                .where(

                    LimitOrder.is_active == True

                )

                .order_by(

                    LimitOrder.created_at.asc()

                )

            )


            return list(result)



    # =====================================
    # УДАЛИТЬ ЗАЯВКУ ПОЛЬЗОВАТЕЛЯ
    # =====================================

    @staticmethod
    def delete_order(

            user_id: int,

            order_id: int

    ) -> bool:


        with SessionLocal() as session:


            order = session.scalar(

                select(LimitOrder)

                .where(

                    LimitOrder.id == order_id,

                    LimitOrder.user_id == user_id

                )

            )


            if order is None:

                return False



            session.delete(order)

            session.commit()


            return True