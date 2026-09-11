"""Эндпоинты оплаты: инициация платежа, вебхук от платёжного провайдера (ЮKassa/CloudPayments и т.п.)."""
from fastapi import APIRouter

router = APIRouter()


@router.post("/init")
async def init_payment():
    # TODO: создать платёж у провайдера, вернуть ссылку/токен для оплаты в mini app
    return {}


@router.post("/webhook")
async def payment_webhook():
    # TODO: принять уведомление об оплате от провайдера, обновить статус заказа
    return {}
