"""
Создаёт базу данных проекта в уже запущенном контейнере Postgres и накатывает schema.sql.

Ничего, кроме Docker и самого контейнера с Postgres, не требуется — скрипт
просто вызывает `docker exec ... psql` из Python, без psycopg2 и прочих зависимостей.

Запуск:
    python create_db.py
    python create_db.py --container my_postgres_container --user postgres

Имя своего контейнера можно посмотреть командой: docker ps
"""
import argparse
import subprocess
import sys
from pathlib import Path

DB_NAME = "673105613811_dom_cvetov"


def run(cmd: list[str], input_bytes: bytes | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, input=input_bytes, capture_output=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--container", default="postgres", help="Имя контейнера с Postgres")
    parser.add_argument("--user", default="postgres", help="Пользователь Postgres")
    parser.add_argument(
        "--maintenance-db",
        default="postgres",
        help="Служебная база для подключения при проверке/создании (обычно 'postgres')",
    )
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    schema_path = script_dir / "schema.sql"

    print(f"Контейнер: {args.container} | Пользователь: {args.user} | База: {DB_NAME}")

    check = run([
        "docker", "exec", "-i", args.container,
        "psql", "-U", args.user, "-d", args.maintenance_db, "-tAc",
        f"SELECT 1 FROM pg_database WHERE datname='{DB_NAME}'",
    ])
    if check.returncode != 0:
        print(check.stderr.decode(errors="replace"))
        sys.exit(1)

    if check.stdout.decode().strip() == "1":
        print(f"База {DB_NAME} уже существует — пропускаю создание.")
    else:
        print(f"Создаю базу {DB_NAME}...")
        create = run([
            "docker", "exec", "-i", args.container,
            "psql", "-U", args.user, "-d", args.maintenance_db,
            "-c", f'CREATE DATABASE "{DB_NAME}";',
        ])
        if create.returncode != 0:
            print(create.stderr.decode(errors="replace"))
            sys.exit(1)

    print("Накатываю schema.sql...")
    apply_result = run(
        ["docker", "exec", "-i", args.container, "psql", "-U", args.user, "-d", DB_NAME],
        input_bytes=schema_path.read_bytes(),
    )
    print(apply_result.stdout.decode(errors="replace"))
    if apply_result.returncode != 0:
        print(apply_result.stderr.decode(errors="replace"))
        sys.exit(1)

    print("Готово. Проверка таблиц:")
    tables = run([
        "docker", "exec", "-i", args.container,
        "psql", "-U", args.user, "-d", DB_NAME, "-c", "\\dt",
    ])
    print(tables.stdout.decode(errors="replace"))


if __name__ == "__main__":
    main()
