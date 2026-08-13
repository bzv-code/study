from sqlalchemy import select, delete, func

from app.database.connect_postgresql import SessionLocal
from app.database.models_postgresql import PortfolioHistory



class PortfolioHistoryRepository:


    # =====================================
    # ДОБАВИТЬ ИСТОРИЮ ПРОДАЖИ
    # =====================================

    @staticmethod
    def add_history(

            user_id: int,

            ticker: str,

            quantity: float,

            buy_price: float,

            sell_price: float,

            buy_total: float,

            sell_total: float,

            profit: float,

            percent: float,

            sell_date

    ) -> PortfolioHistory:


        with SessionLocal() as session:


            history = PortfolioHistory(

                user_id=user_id,

                ticker=ticker.upper(),

                quantity=quantity,

                buy_price=buy_price,

                sell_price=sell_price,

                buy_total=buy_total,

                sell_total=sell_total,

                profit=profit,

                percent=percent,

                sell_date=sell_date

            )


            session.add(history)

            session.commit()

            session.refresh(history)


            return history



    # =====================================
    # ПОЛУЧИТЬ ИСТОРИЮ ПОЛЬЗОВАТЕЛЯ
    # =====================================

    @staticmethod
    def get_user_history(

            user_id: int

    ) -> list[PortfolioHistory]:


        with SessionLocal() as session:


            result = session.scalars(

                select(PortfolioHistory)
                .where(

                    PortfolioHistory.user_id == user_id

                )
                .order_by(

                    PortfolioHistory.created_at.desc()

                )

            )


            return list(result)



    # =====================================
    # ПОЛУЧИТЬ ИСТОРИЮ ПО ТИКЕРУ
    # =====================================

    @staticmethod
    def get_history_by_ticker(

            user_id: int,

            ticker: str

    ) -> list[PortfolioHistory]:


        with SessionLocal() as session:


            result = session.scalars(

                select(PortfolioHistory)
                .where(

                    PortfolioHistory.user_id == user_id,

                    PortfolioHistory.ticker == ticker.upper()

                )
                .order_by(

                    PortfolioHistory.created_at.desc()

                )

            )


            return list(result)



    # =====================================
    # КОЛИЧЕСТВО СДЕЛОК ПОЛЬЗОВАТЕЛЯ
    # =====================================

    @staticmethod
    def count_history(

            user_id: int

    ) -> int:


        with SessionLocal() as session:


            result = session.scalar(

                select(

                    func.count(PortfolioHistory.id)

                )
                .where(

                    PortfolioHistory.user_id == user_id

                )

            )


            return result or 0



    # =====================================
    # ОЧИСТИТЬ ИСТОРИЮ
    # =====================================

    @staticmethod
    def clear_history(

            user_id: int

    ) -> bool:


        with SessionLocal() as session:


            result = session.execute(

                delete(PortfolioHistory)
                .where(

                    PortfolioHistory.user_id == user_id

                )

            )


            session.commit()


            return result.rowcount > 0