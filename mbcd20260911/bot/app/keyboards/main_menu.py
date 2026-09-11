"""Клавиатуры: главное меню бота.

OpenAppButton в maxapi 0.9.4 принимает URL мини-приложения через web_app=
(диплинк вида https://max.ru/<botName>?startapp). Остальные пункты меню —
обычные callback-кнопки (CallbackButton), обработка — в handlers/menu.py.
"""
from maxapi.types import CallbackButton, OpenAppButton
from maxapi.utils.inline_keyboard import InlineKeyboardBuilder

from app.config import settings


def main_menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(
        OpenAppButton(
            text="Каталог букетов",
            web_app=settings.miniapp_deeplink,
        )
    )
    builder.row(CallbackButton(text="Мои заказы", payload="orders"))
    builder.row(CallbackButton(text="Поддержка", payload="support"))
    builder.row(CallbackButton(text="Профиль", payload="profile"))
    return builder.as_markup()
