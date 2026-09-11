"""Pydantic-схемы заказа: создание из корзины mini app и представление для ответа API."""
from pydantic import BaseModel


class OrderItemIn(BaseModel):
    bouquet_id: int
    quantity: int


class OrderCreate(BaseModel):
    items: list[OrderItemIn]
    address: str
    delivery_time: str


class OrderItemOut(BaseModel):
    bouquet_id: int
    quantity: int
    price_at_order: int

    class Config:
        from_attributes = True


class OrderOut(BaseModel):
    id: int
    status: str
    address: str
    delivery_time: str
    total_amount: int
    items: list[OrderItemOut] = []

    class Config:
        from_attributes = True
