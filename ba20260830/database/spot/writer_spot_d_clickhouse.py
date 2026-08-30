import pandas as pd
import numpy as np
from typing import List, Optional

from database.client_clickhouse import client
from .spot_clickhouse import BybitSpotClickHouse

# Имя таблицы должно совпадать с тем, что в create_table
TABLE_NAME = "bybit_spot_d"


def write_spot_d_data_to_clickhouse(
        df: pd.DataFrame,
        chunk_size: int = 50000,
        table_name: Optional[str] = None
) -> bool:
    """
    Принимает DataFrame с данными Bybit и записывает их в ClickHouse чанками.

    Параметры:
    - df: Pandas DataFrame с данными
    - chunk_size: Размер чанка (количество строк за одну вставку).
                  Оптимально для ClickHouse: 50,000 - 100,000.
    - table_name: Имя таблицы (по умолчанию 'bybit_spot_d')

    Возвращает:
    - bool: True если успешно, False если ошибка или DataFrame пуст.
    """
    if df is None or df.empty:
        print("⚠️ DataFrame пуст. Запись в ClickHouse пропущена.")
        return False

    target_table = table_name or TABLE_NAME

    try:
        # Инициализируем репозиторий
        repo = BybitSpotClickHouse(client=client, table_name=target_table)

        # 1. Сбрасываем индекс, чтобы timestamp стал обычной колонкой
        df_reset = df.reset_index()

        # 2. Гарантируем правильный порядок и наличие колонок
        required_columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'coin']

        # Проверяем, что все колонки есть
        missing_cols = [col for col in required_columns if col not in df_reset.columns]
        if missing_cols:
            raise ValueError(f"В DataFrame отсутствуют колонки: {missing_cols}")

        df_clean = df_reset[required_columns].copy()

        # 3. КРИТИЧЕСКИ ВАЖНО: ClickHouse не любит NaN в числовых колонках.
        # Заменяем NaN и NaT на None (который ClickHouse корректно обработает как NULL,
        # если колонка Nullable, или проигнорирует при стандартных типах)
        df_clean = df_clean.replace({np.nan: None, pd.NaT: None})

        total_rows = len(df_clean)
        total_chunks = (total_rows // chunk_size) + (1 if total_rows % chunk_size else 0)

        print(f"🚀 Начало загрузки в ClickHouse: {total_rows} строк, {total_chunks} чанков (по {chunk_size})...")

        successful_chunks = 0

        # 4. Цикл по чанкам
        for i in range(0, total_rows, chunk_size):
            chunk_df = df_clean.iloc[i:i + chunk_size]
            current_chunk_num = (i // chunk_size) + 1

            # Преобразуем только текущий чанк в список кортежей (экономит память)
            data_to_insert = chunk_df.to_records(index=False).tolist()

            # Вставляем чанк
            repo.insert(data=data_to_insert, columns=required_columns)

            successful_chunks += 1
            print(f"   ✅ Чанк {current_chunk_num}/{total_chunks} записан ({len(data_to_insert)} строк)")

        print(f"🎉 Успешно записано всего {total_rows} строк в {repo.get_table_name()}")
        return True

    except Exception as e:
        print(f"❌ Критическая ошибка при записи данных в ClickHouse: {e}")
        return False