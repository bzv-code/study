from app.database.connect_clickhouse_finam import clickhouse_finam


class DividendsRepository:

    TABLE = "dividends"


    def get_future_dividends(self):
        """
        Получить все дивиденды с датами которые еще не наступили
        """

        client = clickhouse_finam.connect()

        print("CLICKHOUSE FINAM DIVIDENDS: future")

        query = f"""
        SELECT
            symbol,
            date,
            amount,
            currency

        FROM {self.TABLE}

        WHERE date >= today()

        ORDER BY date ASC
        """

        result = client.query(query)

        if not result.result_rows:
            return []

        return [
            {
                "ticker": row[0],
                "date": row[1],
                "dividend_amount": row[2],
                "currency": row[3]
            }
            for row in result.result_rows
        ]