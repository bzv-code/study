"""Общие зависимости FastAPI: сессия БД, текущий пользователь по WebAppData из MAX mini app."""
from app.db.session import get_session  # noqa: F401
