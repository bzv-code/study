"""Модель позиции заказа: какой букет, сколько штук, по какой цене на момент заказа.

Цену фиксируем в момент заказа (price_at_order) — если букет потом подорожает
или его вообще уберут из каталога, старые заказы не должны "переехать" по сумме.
"""
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api_app.db.base import Base


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    bouquet_id: Mapped[int] = mapped_column(ForeignKey("bouquets.id"))
    quantity: Mapped[int] = mapped_column()
    price_at_order: Mapped[int] = mapped_column()  # цена букета в копейках на момент заказа

    order: Mapped["Order"] = relationship(back_populates="items")
