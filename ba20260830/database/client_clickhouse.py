# database/client_clickhouse.py
import clickhouse_connect
from .config_clickhouse import config


class ClickHouseClient:
    """Клиент для работы с ClickHouse"""

    def __init__(self):
        self.client = None
        self.config = config

    def connect(self):
        """Устанавливает соединение с ClickHouse"""
        try:
            params = self.config.get_connection_params()
            self.client = clickhouse_connect.get_client(**params)
            print(f"✅ Подключено к {self.config}")
            return self.client
        except Exception as e:
            print(f"❌ Ошибка подключения к ClickHouse: {e}")
            raise

    def disconnect(self):
        """Закрывает соединение"""
        if self.client:
            self.client.close()
            print("🔌 Соединение с ClickHouse закрыто")

    def execute_query(self, query: str, params=None):
        """Выполняет SQL запрос"""
        if not self.client:
            self.connect()

        try:
            result = self.client.query(query, parameters=params)
            return result
        except Exception as e:
            print(f"❌ Ошибка выполнения запроса: {e}")
            raise

    def insert_data(self, table: str, data, column_names=None):
        """Вставляет данные в таблицу"""
        if not self.client:
            self.connect()

        try:
            self.client.insert(table, data, column_names=column_names)
            print(f"✅ Данные вставлены в таблицу {table}")
        except Exception as e:
            print(f"❌ Ошибка вставки данных: {e}")
            raise

    def create_table(self, create_query: str):
        """Создает таблицу"""
        if not self.client:
            self.connect()

        try:
            self.client.command(create_query)
            print("✅ Таблица создана")
        except Exception as e:
            print(f"❌ Ошибка создания таблицы: {e}")
            raise

    def __enter__(self):
        """Поддержка контекстного менеджера (with statement)"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Автоматическое закрытие соединения"""
        self.disconnect()


# Глобальный экземпляр клиента
client = ClickHouseClient()