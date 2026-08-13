from sqlalchemy import (
    select,
    func
)


from app.database.connect_postgresql import SessionLocal
from app.database.models_postgresql import PriceAlert



print(
    "PRICE ALERT REPOSITORY LOADED"
)



class AlertRepository:


    # ==================================================
    # СОЗДАНИЕ УВЕДОМЛЕНИЯ
    # ==================================================

    @staticmethod
    def create(
            user_id: int,
            ticker: str,
            target_price: float,
            condition: str
    ) -> PriceAlert:


        with SessionLocal() as session:


            alert = PriceAlert(

                user_id=user_id,

                ticker=ticker.upper(),

                target_price=target_price,

                condition=condition,

                is_active=True

            )


            session.add(alert)

            session.commit()

            session.refresh(alert)


            return alert



    # ==================================================
    # ВСЕ АКТИВНЫЕ УВЕДОМЛЕНИЯ
    # ==================================================

    @staticmethod
    def get_active() -> list[PriceAlert]:


        with SessionLocal() as session:


            return list(

                session.scalars(

                    select(PriceAlert)

                    .where(

                        PriceAlert.is_active.is_(True)

                    )

                    .order_by(

                        PriceAlert.created_at.asc()

                    )

                ).all()

            )



    # ==================================================
    # УВЕДОМЛЕНИЯ ПОЛЬЗОВАТЕЛЯ
    # ==================================================

    @staticmethod
    def get_user_alerts(
            user_id: int
    ) -> list[PriceAlert]:


        with SessionLocal() as session:


            return list(

                session.scalars(

                    select(PriceAlert)

                    .where(

                        PriceAlert.user_id == user_id

                    )

                    .order_by(

                        PriceAlert.created_at.desc()

                    )

                ).all()

            )



    # ==================================================
    # ОТКЛЮЧЕНИЕ ПОСЛЕ СРАБАТЫВАНИЯ
    # ==================================================

    @staticmethod
    def deactivate(
            alert_id: int
    ) -> PriceAlert | None:


        with SessionLocal() as session:


            alert = session.get(

                PriceAlert,

                alert_id

            )


            if not alert:

                return None



            alert.is_active = False


            session.commit()

            session.refresh(alert)


            return alert



    # ==================================================
    # ПОЛУЧЕНИЕ ПО ID
    # ==================================================

    @staticmethod
    def get_by_id(
            alert_id: int
    ) -> PriceAlert | None:


        with SessionLocal() as session:


            return session.get(

                PriceAlert,

                alert_id

            )



    # ==================================================
    # УДАЛИТЬ УВЕДОМЛЕНИЕ
    # ==================================================

    @staticmethod
    def delete(
            alert_id: int
    ) -> bool:


        with SessionLocal() as session:


            alert = session.get(

                PriceAlert,

                alert_id

            )


            if alert is None:

                return False



            session.delete(alert)

            session.commit()


            return True



    # ==================================================
    # КОЛИЧЕСТВО АКТИВНЫХ УВЕДОМЛЕНИЙ ПОЛЬЗОВАТЕЛЯ
    # ==================================================

    @staticmethod
    def count_active(
            user_id: int
    ) -> int:


        with SessionLocal() as session:


            count = session.scalar(

                select(

                    func.count()

                )

                .select_from(

                    PriceAlert

                )

                .where(

                    PriceAlert.user_id == user_id,

                    PriceAlert.is_active.is_(True)

                )

            )


            return count or 0



    # ==================================================
    # ПРОВЕРКА СУЩЕСТВОВАНИЯ УВЕДОМЛЕНИЯ
    # ==================================================

    @staticmethod
    def exists(
            user_id: int,
            ticker: str
    ) -> bool:


        with SessionLocal() as session:


            result = session.scalar(

                select(PriceAlert)

                .where(

                    PriceAlert.user_id == user_id,

                    PriceAlert.ticker == ticker.upper(),

                    PriceAlert.is_active.is_(True)

                )

            )


            return result is not None