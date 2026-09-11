"""Клавиатуры: главное меню бота.

OpenAppButton принимает URL мини-приложения через web_app= (диплинк вида
https://max.ru/<botName>?startapp[=param]). Каталог и «Мои заказы» ведут на
разные экраны mini app через разные значения start_param — сам роутинг по
нему делается на фронтенде (см. miniapp/src/App.tsx). Остальные пункты меню —
обычные callback-кнопки (CallbackButton), обработка — в handlers/menu.py.
"""
from maxapi.types import CallbackButton, OpenAppButton
from maxapi.utils.inline_keyboard import InlineKeyboardBuilder

from bot_app.config import settings


def main_menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(
        OpenAppButton(
            text="Каталог букетов",
            web_app=settings.miniapp_deeplink(),
        )
    )
    builder.row(
        OpenAppButton(
            text="Мои заказы",
            web_app=settings.miniapp_deeplink("orders"),
        )
    )
    builder.row(CallbackButton(text="Поддержка", payload="support"))
    builder.row(CallbackButton(text="Профиль", payload="profile"))
    return builder.as_markup()
