from database.client_clickhouse import client
from .spot_clickhouse import BybitSpotClickHouse

# Имя таблицы: bybit_spot_d (candles daily)
TABLE_NAME = "bybit_spot_d"


def create_spot_d_table():
    """
    Создает таблицу для дневных свечей спотового рынка Bybit, если её не существует.
    """
    repo = BybitSpotClickHouse(client=client, table_name=TABLE_NAME)

    # Оптимизированная схема для ClickHouse
    create_sql = f"""
    CREATE TABLE IF NOT EXISTS {repo.get_table_name()} (
        timestamp DateTime CODEC(Delta, ZSTD(1)),
        open Float64,
        high Float64,
        low Float64,
        close Float64,
        volume Float64,
        coin LowCardinality(String)
    )
    ENGINE = MergeTree()
    PARTITION BY toYYYYMM(timestamp)
    ORDER BY (coin, timestamp)
    SETTINGS index_granularity = 8192
    """

    print(f"🛠️ Попытка создания таблицы {repo.get_table_name()}...")
    try:
        repo.execute(create_sql)
        print(f"✅ Таблица {repo.get_table_name()} успешно создана или уже существует.")
    except Exception as e:
        print(f"❌ Ошибка при создании таблицы: {e}")


if __name__ == "__main__":
    create_spot_d_table()