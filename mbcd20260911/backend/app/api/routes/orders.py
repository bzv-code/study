"""Эндпоинты заказов: создание заказа из корзины mini app, получение статуса, история пользователя."""
from fastapi import APIRouter

router = APIRouter()


@router.post("")
async def create_order():
    # TODO: создать заказ (позиции, адрес, время доставки, сумма), запустить оплату
    return {}


@router.get("/{order_id}")
async def get_order(order_id: str):
    # TODO: вернуть текущий статус заказа
    return {}


@router.get("")
async def list_user_orders():
    # TODO: вернуть историю заказов текущего пользователя (по max_user_id из WebAppData)
    return []
