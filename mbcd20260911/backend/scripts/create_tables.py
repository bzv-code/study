"""
Накатывает schema.sql на уже существующую базу данных проекта — напрямую по сети,
через psycopg2 (так же, как подключается DBeaver), без Docker и без docker exec.

Установка зависимости (один раз):
    pip install psycopg2-binary

Запуск:
    python create_tables.py --password 7hc70VKhY0OZ
    python create_tables.py --host localhost --port 5432 --dbname 673105613811_dom_cvetov --user super_admin --password ВАШ_ПАРОЛЬ
"""
import argparse
import sys
from pathlib import Path

try:
    import psycopg2
except ImportError:
    print("Не найден psycopg2. Установите: pip install psycopg2-binary")
    sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", default=5432, type=int)
    parser.add_argument("--dbname", default="673105613811_dom_cvetov")
    parser.add_argument("--user", default="super_admin")
    parser.add_argument("--password", required=True, help="Пароль пользователя Postgres")
    args = parser.parse_args()

    schema_path = Path(__file__).resolve().parent / "schema.sql"
    schema_sql = schema_path.read_text(encoding="utf-8")

    print(f"Подключаюсь к {args.host}:{args.port}/{args.dbname} как {args.user}...")

    conn = psycopg2.connect(
        host=args.host,
        port=args.port,
        dbname=args.dbname,
        user=args.user,
        password=args.password,
    )
    conn.autocommit = True

    try:
        with conn.cursor() as cur:
            print("Накатываю schema.sql...")
            cur.execute(schema_sql)

            print("Готово. Проверка таблиц:")
            cur.execute(
                "SELECT table_name FROM information_schema.tables "
                "WHERE table_schema = 'public' ORDER BY table_name;"
            )
            tables = [row[0] for row in cur.fetchall()]
            for t in tables:
                print(f"  - {t}")
            if not tables:
                print("  (таблиц не найдено — что-то пошло не так)")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
