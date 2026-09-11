"""Эндпоинты профиля пользователя: адреса, телефон, бонусы, авторизация через WebAppData MAX."""
from fastapi import APIRouter

router = APIRouter()


@router.get("/me")
async def get_me():
    # TODO: вернуть профиль текущего пользователя
    return {}


@router.put("/me/addresses")
async def update_addresses():
    # TODO: сохранить/обновить адреса доставки пользователя
    return {}
