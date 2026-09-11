"""Бизнес-логика заказов: создание заказа из корзины, пересчёт суммы, смена статуса + уведомление бота."""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api_app.models.bouquet import Bouquet
from api_app.models.order import Order
from api_app.models.order_item import OrderItem
from api_app.schemas.order import OrderCreate


async def create_order_from_cart(session: AsyncSession, user_id: int, payload: OrderCreate) -> Order:
    if not payload.items:
        raise ValueError("Корзина пуста")

    bouquet_ids = [item.bouquet_id for item in payload.items]
    result = await session.execute(select(Bouquet).where(Bouquet.id.in_(bouquet_ids)))
    bouquets_by_id = {b.id: b for b in result.scalars().all()}

    missing = set(bouquet_ids) - set(bouquets_by_id.keys())
    if missing:
        raise ValueError(f"Букеты не найдены: {sorted(missing)}")

    total_amount = sum(
        bouquets_by_id[item.bouquet_id].price * item.quantity for item in payload.items
    )

    order = Order(
        user_id=user_id,
        status="new",
        address=payload.address,
        delivery_time=payload.delivery_time,
        total_amount=total_amount,
    )
    session.add(order)
    await session.flush()  # чтобы получить order.id до коммита

    for item in payload.items:
        session.add(
            OrderItem(
                order_id=order.id,
                bouquet_id=item.bouquet_id,
                quantity=item.quantity,
                price_at_order=bouquets_by_id[item.bouquet_id].price,
            )
        )

    await session.commit()
    await session.refresh(order)
    return order


async def update_order_status(order_id: int, status: str) -> None:
    # TODO: обновить статус в БД и дёрнуть бота (webhook/очередь), чтобы уведомить пользователя
    raise NotImplementedError
