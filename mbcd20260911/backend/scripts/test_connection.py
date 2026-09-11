"""
Проверяет подключение к базе проекта и то, что таблицы на месте (напрямую по сети,
через psycopg2 — так же, как create_tables.py).

По умолчанию сам читает DATABASE_URL из infra/.env — отдельно передавать
хост/пользователя/пароль не нужно. Но при желании их можно переопределить
флагами (например, для подключения к другой базе).

Установка зависимостей (один раз):
    pip install psycopg2-binary python-dotenv

Запуск:
    python test_connection.py
    python test_connection.py --password ДРУГОЙ_ПАРОЛЬ
"""
import argparse
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

EXPECTED_TABLES = {"users", "couriers", "bouquets", "orders"}


def load_connection_defaults() -> dict:
    """Читает .env (пробует несколько вероятных мест) и разбирает DATABASE_URL."""
    project_root = Path(__file__).resolve().parents[2]  # backend/scripts -> backend -> project root

    candidates = [
        project_root / ".env",              # max_bot_dom_cvetov/.env
        project_root / "infra" / ".env",    # max_bot_dom_cvetov/infra/.env
        project_root / "backend" / ".env",  # max_bot_dom_cvetov/backend/.env
    ]

    env_path = next((p for p in candidates if p.exists()), None)
    if env_path is None:
        print("Не нашёл .env ни в одном из мест:")
        for p in candidates:
            print(f"  - {p}")
        print("Беру только значения по умолчанию/из флагов.")
        return {}

    print(f"Нашёл .env: {env_path}")
    load_dotenv(env_path)
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print(f"В {env_path} нет DATABASE_URL — беру только значения по умолчанию/из флагов.")
        return {}

    # postgresql+asyncpg://user:pass@host:port/dbname -> убираем +asyncpg для urlparse
    normalized = database_url.replace("postgresql+asyncpg://", "postgresql://")
    parsed = urlparse(normalized)

    return {
        "host": parsed.hostname,
        "port": parsed.port,
        "dbname": parsed.path.lstrip("/"),
        "user": parsed.username,
        "password": parsed.password,
    }


def main() -> None:
    defaults = load_connection_defaults()

    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default=defaults.get("host", "localhost"))
    parser.add_argument("--port", default=defaults.get("port", 5432), type=int)
    parser.add_argument("--dbname", default=defaults.get("dbname", "673105613811_dom_cvetov"))
    parser.add_argument("--user", default=defaults.get("user", "super_admin"))
    parser.add_argument("--password", default=defaults.get("password"), help="Пароль пользователя Postgres")
    args = parser.parse_args()

    if not args.password:
        print("Пароль не найден ни в infra/.env, ни в флаге --password.")
        sys.exit(1)

    print(f"Подключаюсь к {args.host}:{args.port}/{args.dbname} как {args.user}...")

    try:
        conn = psycopg2.connect(
            host=args.host,
            port=args.port,
            dbname=args.dbname,
            user=args.user,
            password=args.password,
        )
    except psycopg2.OperationalError as e:
        print("Не удалось подключиться:")
        print(e)
        sys.exit(1)

    print("Подключение установлено.\n")

    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT table_name FROM information_schema.tables "
                "WHERE table_schema = 'public' ORDER BY table_name;"
            )
            found_tables = {row[0] for row in cur.fetchall()}

            print("Таблицы в базе:")
            for t in sorted(found_tables):
                print(f"  - {t}")

            missing = EXPECTED_TABLES - found_tables
            if missing:
                print(f"\nВНИМАНИЕ: не хватает таблиц: {', '.join(sorted(missing))}")
            else:
                print("\nВсе ожидаемые таблицы на месте: users, couriers, bouquets, orders.")

            if "bouquets" in found_tables:
                cur.execute("SELECT COUNT(*) FROM public.bouquets;")
                count = cur.fetchone()[0]
                print(f"\nЗапись в bouquets прочиталась успешно, строк сейчас: {count}")
    finally:
        conn.close()
        print("\nСоединение закрыто.")


if __name__ == "__main__":
    main()
