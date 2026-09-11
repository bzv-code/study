"""Общие зависимости FastAPI: сессия БД, текущий пользователь по WebAppData из MAX mini app."""
import json

from fastapi import Depends, Header, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api_app.core.config import settings
from api_app.db.session import get_session
from api_app.models.user import User
from api_app.services.max_auth import parse_init_data


async def get_current_user(
    x_max_init_data: str = Header(default="", alias="X-Max-Init-Data"),
    session: AsyncSession = Depends(get_session),
) -> User:
    """Проверяет WebAppData из заголовка и возвращает пользователя, создавая его при первом обращении."""
    if not x_max_init_data:
        if settings.auth_dev_bypass:
            return await _get_or_create_user(session, max_user_id=999999, full_name="Тестовый пользователь")
        raise HTTPException(status_code=401, detail="Отсутствует X-Max-Init-Data")

    try:
        data = parse_init_data(x_max_init_data, settings.max_bot_token)
    except ValueError:
        raise HTTPException(status_code=401, detail="Невалидная подпись WebAppData")

    raw_user = data.get("user")
    if not raw_user:
        raise HTTPException(status_code=401, detail="В WebAppData нет данных пользователя")

    try:
        user_info = json.loads(raw_user)
        max_user_id = int(user_info["id"])
    except (json.JSONDecodeError, KeyError, ValueError):
        raise HTTPException(status_code=401, detail="Не удалось разобрать данные пользователя")

    full_name = " ".join(filter(None, [user_info.get("first_name"), user_info.get("last_name")]))
    return await _get_or_create_user(session, max_user_id=max_user_id, full_name=full_name)


async def _get_or_create_user(session: AsyncSession, max_user_id: int, full_name: str) -> User:
    result = await session.execute(select(User).where(User.max_user_id == max_user_id))
    user = result.scalar_one_or_none()

    if user is None:
        user = User(max_user_id=max_user_id, full_name=full_name)
        session.add(user)
        await session.commit()
        await session.refresh(user)

    return user
