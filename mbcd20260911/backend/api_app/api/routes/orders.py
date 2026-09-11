"""Эндпоинты заказов: создание заказа из корзины mini app, получение статуса, история пользователя."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api_app.api.deps import get_current_user
from api_app.db.session import get_session
from api_app.models.order import Order
from api_app.models.user import User
from api_app.schemas.order import OrderCreate, OrderOut
from api_app.services.order_service import create_order_from_cart

router = APIRouter()


@router.post("", response_model=OrderOut)
async def create_order(
    payload: OrderCreate,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    try:
        order = await create_order_from_cart(session, user.id, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return order


@router.get("/{order_id}", response_model=OrderOut)
async def get_order(
    order_id: int,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    order = await session.get(Order, order_id)
    if order is None or order.user_id != user.id:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return order


@router.get("", response_model=list[OrderOut])
async def list_user_orders(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(
        select(Order).where(Order.user_id == user.id).order_by(Order.id.desc())
    )
    return result.scalars().all()
