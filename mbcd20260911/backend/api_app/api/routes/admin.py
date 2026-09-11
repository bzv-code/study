"""Эндпоинты для админки/CRM: список всех заказов, смена статуса, назначение курьера, управление каталогом."""
from fastapi import APIRouter

router = APIRouter()


@router.get("/orders")
async def admin_list_orders():
    # TODO: вернуть все заказы с фильтрами по статусу/дате для оператора
    return []


@router.patch("/orders/{order_id}/status")
async def admin_update_order_status(order_id: str):
    # TODO: обновить статус заказа и уведомить пользователя через бота
    return {}
