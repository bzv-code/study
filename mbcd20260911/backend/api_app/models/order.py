"""Модель заказа: пользователь, позиции, адрес, время доставки, статус, сумма, курьер."""
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api_app.db.base import Base
from api_app.models.order_item import OrderItem


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    status: Mapped[str] = mapped_column(String(50), default="new")
    address: Mapped[str] = mapped_column(String(500))
    delivery_time: Mapped[str] = mapped_column(String(100))
    total_amount: Mapped[int] = mapped_column()
    courier_id: Mapped[int | None] = mapped_column(ForeignKey("couriers.id"), nullable=True)

    items: Mapped[list[OrderItem]] = relationship(back_populates="order", lazy="selectin")
