import clickhouse_connect

from app.config import settings


class ClickHouseFinamConnection:

    def __init__(self):
        self.client = None


    def connect(self):

        if self.client is None:

            self.client = clickhouse_connect.get_client(
                host=settings.CLICKHOUSE_FINAM_HOST,
                port=settings.CLICKHOUSE_FINAM_PORT,
                username=settings.CLICKHOUSE_FINAM_USER,
                password=settings.CLICKHOUSE_FINAM_PASSWORD,
                database=settings.CLICKHOUSE_FINAM_DATABASE
            )

        return self.client


    def close(self):

        if self.client:

            self.client.close()
            self.client = None



clickhouse_finam = ClickHouseFinamConnection()