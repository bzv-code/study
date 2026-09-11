#!/usr/bin/env bash
# Создаёт базу данных проекта в уже работающем контейнере Postgres и накатывает schema.sql.
#
# Использование:
#   ./create_db.sh [имя_контейнера] [пользователь_postgres]
#
# По умолчанию: контейнер "postgres", пользователь "postgres".
# Имя своего контейнера можно посмотреть командой: docker ps
set -euo pipefail

CONTAINER_NAME="${1:-postgres}"
DB_USER="${2:-postgres}"
DB_NAME="673105613811_dom_cvetov"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Контейнер: $CONTAINER_NAME | Пользователь: $DB_USER | База: $DB_NAME"

EXISTS=$(docker exec -i "$CONTAINER_NAME" psql -U "$DB_USER" -tAc \
  "SELECT 1 FROM pg_database WHERE datname='${DB_NAME}'")

if [ "$EXISTS" = "1" ]; then
  echo "База ${DB_NAME} уже существует — пропускаю создание."
else
  echo "Создаю базу ${DB_NAME}..."
  docker exec -i "$CONTAINER_NAME" psql -U "$DB_USER" -c "CREATE DATABASE \"${DB_NAME}\";"
fi

echo "Накатываю schema.sql..."
cat "$SCRIPT_DIR/schema.sql" | docker exec -i "$CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME"

echo "Готово. Проверка таблиц:"
docker exec -i "$CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME" -c "\dt"
