"""Модель заказа: пользователь, позиции, адрес, время доставки, статус, сумма, курьер."""
from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    status: Mapped[str] = mapped_column(String(50), default="new")
    address: Mapped[str] = mapped_column(String(500))
    delivery_time: Mapped[str] = mapped_column(String(100))
    total_amount: Mapped[int] = mapped_column()
    courier_id: Mapped[int | None] = mapped_column(ForeignKey("couriers.id"), nullable=True)
