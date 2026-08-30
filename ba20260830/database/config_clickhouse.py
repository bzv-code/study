# database/config_clickhouse.py
import os
from dotenv import load_dotenv
from pathlib import Path

# Загружаем .env файл из корня проекта
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)


class ClickHouseConfig:
    """Конфигурация подключения к ClickHouse"""

    def __init__(self):
        self.host = os.getenv('CLICKHOUSE_HOST', 'localhost')
        self.port = int(os.getenv('CLICKHOUSE_PORT', '8123'))
        self.user = os.getenv('CLICKHOUSE_USER', 'default')
        self.password = os.getenv('CLICKHOUSE_PASSWORD', '')
        self.database = os.getenv('CLICKHOUSE_DATABASE', 'default')

    def get_connection_params(self) -> dict:
        """Возвращает параметры подключения в виде словаря"""
        return {
            'host': self.host,
            'port': self.port,
            'username': self.user,
            'password': self.password,
            'database': self.database
        }

    def __str__(self):
        return f"ClickHouse({self.host}:{self.port}/{self.database})"


# Глобальный экземпляр конфигурации
config = ClickHouseConfig()