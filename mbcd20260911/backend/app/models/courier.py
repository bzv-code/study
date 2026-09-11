"""Модель курьера: имя, телефон, статус доступности."""
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Courier(Base):
    __tablename__ = "couriers"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(200))
    phone: Mapped[str] = mapped_column(String(30))
    is_available: Mapped[bool] = mapped_column(default=True)
