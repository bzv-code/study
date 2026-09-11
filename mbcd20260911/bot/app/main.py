"""Точка входа бота: инициализация диспетчера, регистрация роутеров, запуск polling.

Само мини-приложение (каталог/корзина) в чате открывается кнопкой OpenAppButton
из главного меню (см. keyboards/main_menu.py), ссылающейся на диплинк вида
https://max.ru/<botName>?startapp. URL, куда ведёт этот диплинк, дополнительно
настраивается в кабинете бота на платформе MAX для партнёров.
"""
import asyncio
import logging
import sys
from pathlib import Path

# Делает импорты вида "from app.config import ..." рабочими независимо от того,
# запущен ли файл напрямую (клик в PyCharm) или как модуль (python -m app.main).
# Без этого прямой запуск файла падает с "ModuleNotFoundError: No module named 'app.config'".
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from maxapi import Bot, Dispatcher

from app.config import settings
from app.handlers import menu, start


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

    if not settings.bot_token:
        logging.error(
            "MAX_BOT_TOKEN пустой — проверьте, что .env лежит в корне проекта, "
            "infra/ или bot/, и содержит строку MAX_BOT_TOKEN=..."
        )
        return

    bot = Bot(settings.bot_token)
    dp = Dispatcher()

    dp.include_routers(
        start.router,
        menu.router,
    )

    logging.info("Bot started")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
