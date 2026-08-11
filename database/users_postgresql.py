from sqlalchemy import select

from app.database.connect_postgresql import SessionLocal
from app.database.models_postgresql import User


class UserRepository:

    @staticmethod
    def get(max_user_id: int) -> User | None:

        with SessionLocal() as session:

            return session.scalar(
                select(User).where(
                    User.max_user_id == max_user_id
                )
            )

    @staticmethod
    def create(
        max_user_id: int,
        first_name: str | None,
        last_name: str | None,
        username: str | None,
    ) -> User:

        with SessionLocal() as session:

            user = User(
                max_user_id=max_user_id,
                first_name=first_name,
                last_name=last_name,
                username=username,
            )

            session.add(user)
            session.commit()
            session.refresh(user)

            return user

    @staticmethod
    def get_or_create(
        max_user_id: int,
        first_name: str | None,
        last_name: str | None,
        username: str | None,
    ) -> User:

        user = UserRepository.get(max_user_id)

        if user:
            return user

        return UserRepository.create(
            max_user_id=max_user_id,
            first_name=first_name,
            last_name=last_name,
            username=username,
        )

    @staticmethod
    def all() -> list[User]:

        with SessionLocal() as session:

            return list(
                session.scalars(
                    select(User)
                )
            )