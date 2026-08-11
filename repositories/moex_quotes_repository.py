from app.database.connect_clickhouse import clickhouse


class MoexQuotesRepository:

    TABLE = "finam_api.moex_quotes_d"


    def get_last_quote(self, ticker: str):

        client = clickhouse.connect()


        print(
            "CLICKHOUSE QUOTE:",
            ticker
        )


        query = f"""
        SELECT
            ticker,
            name,
            date,
            close,
            sector

        FROM {self.TABLE}

        WHERE ticker = %(ticker)s

        ORDER BY date DESC

        LIMIT 1
        """


        result = client.query(
            query,
            parameters={
                "ticker": ticker
            }
        )


        if not result.result_rows:
            return None


        row = result.result_rows[0]


        return {

            "ticker": row[0],
            "name": row[1],
            "date": row[2],
            "close": row[3],
            "sector": row[4]

        }



    def get_history(
            self,
            ticker: str,
            limit: int = 30
    ):


        client = clickhouse.connect()


        print(
            "CLICKHOUSE HISTORY:",
            ticker
        )


        query = f"""

        SELECT

            date,
            open,
            high,
            low,
            close,
            volume

        FROM {self.TABLE}

        WHERE ticker = %(ticker)s

        ORDER BY date DESC

        LIMIT %(limit)s

        """


        result = client.query(

            query,

            parameters={

                "ticker": ticker,
                "limit": limit

            }

        )


        if not result.result_rows:
            return []


        return [

            {
                "date": row[0],
                "open": row[1],
                "high": row[2],
                "low": row[3],
                "close": row[4],
                "volume": row[5]
            }

            for row in result.result_rows

        ]

    # ==================================================
    # ИСТОРИЯ ВСЕГО РЫНКА
    # ==================================================

    def get_market_history(

            self,

            limit: int = 7

    ):

        client = clickhouse.connect()

        print(

            "CLICKHOUSE MARKET HISTORY DAYS:",

            limit

        )

        query = f"""

        SELECT

            ticker,

            name,

            sector,

            date,

            close,

            volume


        FROM {self.TABLE}


        WHERE date >= (

            SELECT max(date)

            FROM {self.TABLE}

        ) - INTERVAL %(limit)s DAY


        ORDER BY

            ticker,

            date DESC


        """

        result = client.query(

            query,

            parameters={

                "limit": limit

            }

        )

        if not result.result_rows:
            return []

        return [

            {

                "ticker": row[0],

                "name": row[1],

                "sector": row[2],

                "date": row[3],

                "close": row[4],

                "volume": row[5]

            }

            for row in result.result_rows

        ]