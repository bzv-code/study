"""Настройки админ-панели: пути, учётные данные администратора, секрет JWT."""
import os
import secrets
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent  # admin-panel/server

# SQLite-база рядом с сервером (самодостаточный MVP-домен админки)
DATABASE_PATH = BASE_DIR / "admin_panel.db"

# Секрет для подписи JWT. В проде задайте стабильный ADMIN_SECRET_KEY в окружении,
# иначе после перезапуска сервера все выданные токены станут недействительны.
SECRET_KEY = os.getenv("ADMIN_SECRET_KEY", secrets.token_hex(32))
TOKEN_TTL_MINUTES = 12 * 60  # сессия живёт 12 часов

# Учётная запись администратора по умолчанию.
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")

# Папка для загруженных картинок товаров (раздаётся статикой по /static/uploads/...)
UPLOADS_DIR = BASE_DIR / "uploads"
UPLOADS_DIR.mkdir(exist_ok=True)
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5 МБ
