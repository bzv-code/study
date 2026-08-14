import clickhouse_connect

from app.config import settings


class ClickHouseConnection:

    def __init__(self):
        self.client = None


    def connect(self):

        if self.client is None:

            self.client = clickhouse_connect.get_client(
                host=settings.CLICKHOUSE_HOST,
                port=settings.CLICKHOUSE_PORT,
                username=settings.CLICKHOUSE_USER,
                password=settings.CLICKHOUSE_PASSWORD,
                database=settings.CLICKHOUSE_DATABASE
            )

        return self.client


    def close(self):

        if self.client:

            self.client.close()
            self.client = None



clickhouse = ClickHouseConnection()