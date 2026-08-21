from sqlalchemy import select, delete

from app.database.connect_postgresql import SessionLocal
from app.database.models_postgresql import Portfolio


class PortfolioRepository:


    # =====================================
    # ДОБАВИТЬ ПОЗИЦИЮ
    # =====================================

    @staticmethod
    def add_position(

            user_id: int,
            ticker: str,
            quantity: float,
            buy_price: float,
            buy_date

    ) -> Portfolio:


        with SessionLocal() as session:


            position = Portfolio(

                user_id=user_id,

                ticker=ticker.upper(),

                quantity=quantity,

                buy_price=buy_price,

                buy_date=buy_date

            )


            session.add(position)

            session.commit()

            session.refresh(position)


            return position



    # =====================================
    # ПОЛУЧИТЬ ПОРТФЕЛЬ ПОЛЬЗОВАТЕЛЯ
    # =====================================

    @staticmethod
    def get_user_portfolio(

            user_id: int

    ) -> list[Portfolio]:


        with SessionLocal() as session:


            result = session.scalars(

                select(Portfolio)
                .where(

                    Portfolio.user_id == user_id

                )
                .order_by(

                    Portfolio.created_at.desc()

                )

            )


            return list(result)



    # =====================================
    # НАЙТИ АКЦИЮ
    # =====================================

    @staticmethod
    def get_position(

            user_id: int,

            ticker: str

    ) -> Portfolio | None:


        with SessionLocal() as session:


            return session.scalar(

                select(Portfolio)
                .where(

                    Portfolio.user_id == user_id,

                    Portfolio.ticker == ticker.upper()

                )

            )



    # =====================================
    # УДАЛИТЬ ВСЕ ПОКУПКИ ПО ТИКЕРУ
    # =====================================

    @staticmethod
    def delete_by_ticker(

            user_id: int,

            ticker: str

    ) -> bool:


        with SessionLocal() as session:


            result = session.execute(

                delete(Portfolio)
                .where(

                    Portfolio.user_id == user_id,

                    Portfolio.ticker == ticker.upper()

                )

            )


            session.commit()


            return result.rowcount > 0



    # =====================================
    # УМЕНЬШИТЬ ПОЗИЦИЮ
    # Продажа части акций
    # =====================================

    @staticmethod
    def reduce_position(

            user_id: int,

            ticker: str,

            quantity: float

    ) -> Portfolio | bool | None:


        with SessionLocal() as session:


            position = session.scalar(

                select(Portfolio)
                .where(

                    Portfolio.user_id == user_id,

                    Portfolio.ticker == ticker.upper()

                )

            )


            # позиция отсутствует

            if position is None:

                return None



            # защита от некорректного количества

            if quantity <= 0:

                return None



            # нельзя продать больше чем есть

            if quantity > position.quantity:

                return None



            # уменьшаем количество

            position.quantity -= quantity



            # если продали всю позицию

            if position.quantity <= 0:


                session.delete(position)

                session.commit()


                return True



            session.commit()

            session.refresh(position)


            return position