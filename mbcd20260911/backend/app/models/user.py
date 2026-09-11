"""Модель пользователя: max_user_id, имя, телефон, адреса, бонусный баланс."""
from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    # В личном чате с ботом MAX chat_id совпадает с id пользователя,
    # поэтому это же значение используется и для отправки уведомлений ботом.
    max_user_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(200), default="")
    phone: Mapped[str] = mapped_column(String(30), default="")
    bonus_balance: Mapped[int] = mapped_column(default=0)
