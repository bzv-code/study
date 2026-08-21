from app.database.connect_clickhouse import clickhouse


class MoexQuotesRepository:

    TABLE = "moex_api.moex_stock_d"

    def get_last_quote(self, ticker: str):
        client = clickhouse.connect()

        print("CLICKHOUSE QUOTE:", ticker)

        query = f"""
        SELECT
            secid AS ticker,
            shortname AS name,
            date,
            close,
            sector

        FROM {self.TABLE}

        WHERE secid = %(ticker)s
          AND engine = 'stock'
          AND market = 'shares'

        ORDER BY date DESC

        LIMIT 1
        """

        result = client.query(
            query,
            parameters={"ticker": ticker}
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

    def get_history(self, ticker: str, limit: int = 30):
        client = clickhouse.connect()

        print("CLICKHOUSE HISTORY:", ticker)

        query = f"""
        SELECT
            date,
            open,
            high,
            low,
            close,
            volume

        FROM {self.TABLE}

        WHERE secid = %(ticker)s
          AND engine = 'stock'
          AND market = 'shares'

        ORDER BY date DESC

        LIMIT %(limit)s
        """

        result = client.query(
            query,
            parameters={"ticker": ticker, "limit": limit}
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

    def get_market_history(self, limit: int = 7):
        client = clickhouse.connect()

        print("CLICKHOUSE MARKET HISTORY DAYS:", limit)

        query = f"""
        SELECT
            secid AS ticker,
            shortname AS name,
            sector,
            date,
            close,
            volume

        FROM {self.TABLE}

        WHERE engine = 'stock'
          AND market = 'shares'
          AND date >= (
              SELECT max(date)
              FROM {self.TABLE}
              WHERE engine = 'stock' AND market = 'shares'
          ) - INTERVAL %(limit)s DAY

        ORDER BY
            secid,
            date DESC
        """

        result = client.query(
            query,
            parameters={"limit": limit}
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

    def get_hourly_history(self, ticker: str, limit: int = 24):
        """
        Получить почасовые данные за последний день
        из таблицы moex_stock_h1

        Используется для построения графика за период 1 день
        """

        client = clickhouse.connect()

        print("CLICKHOUSE HOURLY HISTORY:", ticker)

        query = f"""
        SELECT
            date,
            open,
            high,
            low,
            close,
            volume

        FROM moex_stock_h1

        WHERE secid = %(ticker)s
          AND engine = 'stock'
          AND market = 'shares'

        ORDER BY date DESC

        LIMIT %(limit)s
        """

        result = client.query(
            query,
            parameters={"ticker": ticker, "limit": limit}
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

    def get_weekly_history(self, ticker: str, limit: int = 180):
        """
        Получить недельные данные из таблицы moex_stock_h

        Используется для построения графика за период 180 дней
        (недельные данные = меньше точек на графике)
        """

        client = clickhouse.connect()

        print("CLICKHOUSE WEEKLY HISTORY:", ticker)

        query = f"""
        SELECT
            date,
            open,
            high,
            low,
            close,
            volume

        FROM moex_stock_h

        WHERE secid = %(ticker)s
          AND engine = 'stock'
          AND market = 'shares'

        ORDER BY date DESC

        LIMIT %(limit)s
        """

        result = client.query(
            query,
            parameters={"ticker": ticker, "limit": limit}
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

    def get_last_quote_m10(self, ticker: str):
        """
        Получить последнюю цену из 10-минутной таблицы moex_stock_m10

        Данные в таблице хранятся по московскому времени
        (колонка date = DateTime('Europe/Moscow'))

        Используется для проверки уведомлений
        """

        client = clickhouse.connect()

        print("CLICKHOUSE QUOTE M10:", ticker)

        query = f"""
        SELECT
            secid AS ticker,
            date,
            close

        FROM moex_api.moex_stock_m10

        WHERE secid = %(ticker)s
          AND engine = 'stock'
          AND market = 'shares'

        ORDER BY date DESC

        LIMIT 1
        """

        result = client.query(
            query,
            parameters={"ticker": ticker}
        )

        if not result.result_rows:
            return None

        row = result.result_rows[0]

        return {
            "ticker": row[0],
            "date": row[1],
            "close": row[2]
        }

    def get_recent_bars_m10(self, ticker: str, limit: int = 10):
        """
        Получить максимумы (high) последних баров m10

        Используется для проверки лимитных заявок:
        если хотя бы один из последних 10 баров
        превысил цену заявки — заявка исполняется
        """

        client = clickhouse.connect()

        print("CLICKHOUSE M10 BARS:", ticker)

        query = f"""
        SELECT
            high

        FROM moex_api.moex_stock_m10

        WHERE secid = %(ticker)s
          AND engine = 'stock'
          AND market = 'shares'

        ORDER BY date DESC

        LIMIT %(limit)s
        """

        result = client.query(
            query,
            parameters={"ticker": ticker, "limit": limit}
        )

        if not result.result_rows:
            return []

        return [
            float(row[0])
            for row in result.result_rows
        ]

    def get_year_stocks(self):
        """
        Уникальные акции с начала года
        из таблицы moex_stock_d
        """

        client = clickhouse.connect()

        print("CLICKHOUSE YEAR STOCKS")

        query = f"""
        SELECT
            secid,
            any(name) AS name

        FROM {self.TABLE}

        WHERE engine = 'stock'
          AND market = 'shares'
          AND date >= toStartOfYear(today())

        GROUP BY secid

        ORDER BY secid ASC
        """

        result = client.query(query)

        if not result.result_rows:
            return []

        return [
            {
                "ticker": row[0],
                "name": row[1]
            }
            for row in result.result_rows
        ]



    def get_year_sectors(self):
        """
        Уникальные сектора и акции с начала года
        из таблицы moex_stock_d
        """

        client = clickhouse.connect()

        print("CLICKHOUSE YEAR SECTORS")

        query = f"""
        SELECT
            sector,
            secid,
            any(name) AS name

        FROM {self.TABLE}

        WHERE engine = 'stock'
          AND market = 'shares'
          AND date >= toStartOfYear(today())

        GROUP BY sector, secid

        ORDER BY sector ASC, secid ASC
        """

        result = client.query(query)

        if not result.result_rows:
            return []

        return [
            {
                "sector": row[0],
                "ticker": row[1],
                "name": row[2]
            }
            for row in result.result_rows
        ]