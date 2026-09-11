"""
Наполняет таблицу bouquets тестовыми букетами (для проверки каталога).

Сам находит .env (корень проекта / infra/ / backend/) и берёт DATABASE_URL оттуда,
как и test_connection.py. Идемпотентно: не создаёт дубликаты, если букет с таким
title уже есть — просто пропускает.

Запуск:
    python seed_bouquets.py
"""
import sys
from pathlib import Path
from urllib.parse import urlparse

try:
    import psycopg2
except ImportError:
    print("Не найден psycopg2. Установите: pip install psycopg2-binary")
    sys.exit(1)

try:
    from dotenv import load_dotenv
except ImportError:
    print("Не найден python-dotenv. Установите: pip install python-dotenv")
    sys.exit(1)

import os

SAMPLE_BOUQUETS = [
    # title, category, description, price (в копейках), photo_url
    (
        "Розовое настроение",
        "romance",
        "15 розовых пионовидных роз, эвкалипт, крафт-бумага",
        290000,
        "https://example.com/photos/bouquet-1.jpg",
    ),
    (
        "Для мамы",
        "for_mom",
        "Хризантемы, герберы и альстромерии в нежных тонах",
        190000,
        "https://example.com/photos/bouquet-2.jpg",
    ),
    (
        "Свадебный",
        "wedding",
        "Белые розы, эустома, зелень, атласная лента",
        450000,
        "https://example.com/photos/bouquet-3.jpg",
    ),
    (
        "Просто так",
        "no_reason",
        "Яркий микс из тюльпанов и ромашек",
        120000,
        "https://example.com/photos/bouquet-4.jpg",
    ),
]


def load_database_url() -> str:
    project_root = Path(__file__).resolve().parents[2]
    candidates = [
        project_root / ".env",
        project_root / "infra" / ".env",
        project_root / "backend" / ".env",
    ]
    env_path = next((p for p in candidates if p.exists()), None)
    if env_path is None:
        print("Не нашёл .env ни в одном из мест:")
        for p in candidates:
            print(f"  - {p}")
        sys.exit(1)

    print(f"Нашёл .env: {env_path}")
    load_dotenv(env_path)
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print(f"В {env_path} нет DATABASE_URL")
        sys.exit(1)
    return database_url


def main() -> None:
    database_url = load_database_url()
    normalized = database_url.replace("postgresql+asyncpg://", "postgresql://")
    parsed = urlparse(normalized)

    print(f"Подключаюсь к {parsed.hostname}:{parsed.port}/{parsed.path.lstrip('/')}...")
    conn = psycopg2.connect(
        host=parsed.hostname,
        port=parsed.port,
        dbname=parsed.path.lstrip("/"),
        user=parsed.username,
        password=parsed.password,
    )
    conn.autocommit = True

    try:
        with conn.cursor() as cur:
            added = 0
            for title, category, description, price, photo_url in SAMPLE_BOUQUETS:
                cur.execute("SELECT 1 FROM public.bouquets WHERE title = %s;", (title,))
                if cur.fetchone():
                    print(f"  пропускаю (уже есть): {title}")
                    continue

                cur.execute(
                    """
                    INSERT INTO public.bouquets (title, category, description, price, photo_url)
                    VALUES (%s, %s, %s, %s, %s);
                    """,
                    (title, category, description, price, photo_url),
                )
                print(f"  добавлен: {title}")
                added += 1

            print(f"\nГотово. Добавлено новых букетов: {added}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
