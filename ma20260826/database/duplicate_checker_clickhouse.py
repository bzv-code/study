
from __future__ import annotations


from datetime import datetime
from typing import Any


from database.client_clickhouse import (
    ClickHouseClient,
)


from utils.datetime_utils import (
    parse_moscow_datetime,
)


from utils.logger import get_logger


logger = get_logger(__name__)


class _LazyExistingKeys:
    """
    Ленивый контейнер существующих ключей.

    Нужен для обратной совместимости
    со всеми существующими Writer.

    Старый код Writer:

        existing_keys = (
            duplicate_checker.load_existing_keys(...)
        )

    продолжает работать без изменений.

    ВАЖНО:

    Реальные ключи из ClickHouse здесь
    НЕ загружаются.

    Они загружаются только внутри
    filter_new_rows(), когда уже известны
    строки текущего пакета.

    Благодаря этому можно построить
    оптимизированный запрос:

        SECID + диапазон дат
    """


    def __init__(
        self,
        checker: "DuplicateCheckerClickHouse",
        table: str,
        key_columns: list[str],
    ) -> None:

        self.checker = checker
        self.table = table
        self.key_columns = key_columns


    def __iter__(self):
        """
        Совместимость с set.

        Реальные данные загружаются
        внутри filter_new_rows().
        """

        return iter(())


    def __len__(self) -> int:
        """
        Для совместимости.

        До выполнения filter_new_rows()
        количество ключей неизвестно.
        """

        return 0


class DuplicateCheckerClickHouse:
    """
    Универсальная проверка дублей ClickHouse.

    Оптимизированная логика:

    1. НЕ загружает ключи всей таблицы.

    2. Получает строки текущей загрузки.

    3. Определяет:
       - минимальную дату;
       - максимальную дату;
       - SECID.

    4. Запрашивает из ClickHouse
       только существующие ключи
       конкретного SECID в конкретном
       диапазоне дат.

    5. Проверяет дубли внутри
       текущего пакета.

    6. Не требует изменений
       существующих Writer.

    Пример:

        SECID = SIU6

        FROM = 2024-11-26
        TO   = 2026-07-31

    Выполняется:

        SELECT secid, date
        FROM table
        WHERE secid = 'SIU6'
          AND date >= '2024-11-26'
          AND date <= '2026-07-31'

    Вместо:

        SELECT secid, date
        FROM table

    по всей таблице.

    Все datetime приводятся
    к московскому времени
    без timezone.
    """


    DATETIME_COLUMNS = {

        "date",

        "begin",

        "end",

        "datetime",

    }


    def __init__(
        self,
        client: ClickHouseClient,
    ) -> None:

        self.client = client

        logger.debug(
            "DuplicateCheckerClickHouse initialized"
        )


    # ==================================================
    # DATETIME
    # ==================================================

    @staticmethod
    def _normalize_datetime(
        value: Any,
    ) -> datetime:
        """
        Приведение datetime
        к единому виду.

        UTC / naive / Moscow

        ->

        Europe/Moscow

        ->

        naive datetime.
        """

        dt = parse_moscow_datetime(
            value
        )

        return dt.replace(
            tzinfo=None
        )


    # ==================================================
    # LOAD EXISTING KEYS
    # ==================================================

    def load_existing_keys(
        self,
        table: str,
        key_columns: list[str],
    ) -> set[tuple]:
        """
        Совместимый интерфейс старого Writer.

        Раньше здесь выполнялся запрос
        всей таблицы:

            SELECT secid, date
            FROM table

        При 60+ млн строк это очень дорого.

        Теперь возвращается ленивый объект.

        Реальный запрос будет выполнен
        позже в filter_new_rows().
        """

        if not key_columns:

            logger.warning(
                "LOAD EXISTING KEYS SKIPPED: "
                "EMPTY KEY COLUMNS"
            )

            return set()


        logger.info(
            "PREPARE LAZY EXISTING KEYS TABLE=%s",
            table,
        )

        logger.debug(
            "KEY COLUMNS=%s",
            key_columns,
        )


        print("=" * 80)
        print("PREPARE EXISTING KEYS")
        print("=" * 80)

        print(
            f"TABLE: {table}"
        )

        print(
            f"KEYS : {', '.join(key_columns)}"
        )

        print(
            "MODE : RANGE / SECID OPTIMIZED"
        )


        return _LazyExistingKeys(
            checker=self,
            table=table,
            key_columns=key_columns,
        )


    # ==================================================
    # DATETIME COLUMN
    # ==================================================

    @classmethod
    def _find_datetime_column(
        cls,
        key_columns: list[str],
    ) -> str | None:
        """
        Ищет datetime-колонку
        среди ключевых колонок.
        """

        for column in key_columns:

            if column in cls.DATETIME_COLUMNS:

                return column


        return None


    # ==================================================
    # DATE RANGE
    # ==================================================

    @classmethod
    def _get_datetime_range(
        cls,
        rows: list[list[Any]],
        columns: list[str],
        datetime_column: str,
    ) -> tuple[datetime, datetime] | None:
        """
        Определяет минимальную
        и максимальную дату
        текущего пакета.
        """

        if not rows:
            return None


        if datetime_column not in columns:
            return None


        index = columns.index(
            datetime_column
        )


        dates: list[datetime] = []


        for row in rows:

            if index >= len(row):
                continue


            value = row[index]


            if value is None:
                continue


            try:

                dt = cls._normalize_datetime(
                    value
                )

            except Exception:

                logger.warning(
                    "DATETIME NORMALIZATION ERROR "
                    "COLUMN=%s VALUE=%s",
                    datetime_column,
                    value,
                )

                continue


            dates.append(dt)


        if not dates:
            return None


        return (
            min(dates),
            max(dates),
        )


    # ==================================================
    # UNIQUE KEY VALUES
    # ==================================================

    @staticmethod
    def _get_unique_values(
        rows: list[list[Any]],
        columns: list[str],
        column: str,
    ) -> list[Any]:
        """
        Получает уникальные значения
        указанной ключевой колонки
        из текущего пакета.
        """

        if column not in columns:
            return []


        index = columns.index(
            column
        )


        values = set()


        for row in rows:

            if index >= len(row):
                continue


            value = row[index]


            if value is None:
                continue


            values.add(value)


        return list(values)


    # ==================================================
    # SQL VALUE
    # ==================================================

    @staticmethod
    def _escape_sql_string(
        value: str,
    ) -> str:
        """
        Безопасное экранирование
        строкового значения для SQL.
        """

        return (
            value
            .replace(
                "\\",
                "\\\\",
            )
            .replace(
                "'",
                "\\'",
            )
        )


    @classmethod
    def _format_sql_value(
        cls,
        value: Any,
    ) -> str:
        """
        Формирование значения
        для SQL WHERE.
        """

        if isinstance(value, str):

            return (
                "'"
                + cls._escape_sql_string(value)
                + "'"
            )


        if isinstance(value, bool):

            return (
                "1"
                if value
                else "0"
            )


        return str(value)


    # ==================================================
    # LOAD RANGE KEYS
    # ==================================================

    def _load_existing_keys_for_range(
        self,
        lazy_keys: _LazyExistingKeys,
        rows: list[list[Any]],
        columns: list[str],
    ) -> set[tuple]:
        """
        Загружает существующие ключи
        только для SECID и диапазона
        текущей загрузки.

        Например:

            SECID = SIU6

            FROM = 2024-11-26
            TO   = 2026-07-31

        Запрос:

            SELECT secid, date
            FROM table
            WHERE date >= ...
              AND date <= ...
              AND secid = ...

        Если данных нет:

            возвращается пустой set.

        Если данные есть:

            загружаются только ключи
            этого SECID и диапазона.
        """

        table = lazy_keys.table

        key_columns = lazy_keys.key_columns


        # --------------------------------------------------
        # DATETIME COLUMN
        # --------------------------------------------------

        datetime_column = (
            self._find_datetime_column(
                key_columns
            )
        )


        if datetime_column is None:

            logger.warning(
                "NO DATETIME KEY COLUMN "
                "FALLBACK TO FULL KEY LOAD"
            )

            return self._load_existing_keys_full(
                table=table,
                key_columns=key_columns,
            )


        # --------------------------------------------------
        # DATE RANGE
        # --------------------------------------------------

        date_range = self._get_datetime_range(
            rows=rows,
            columns=columns,
            datetime_column=datetime_column,
        )


        if date_range is None:

            logger.warning(
                "DATE RANGE NOT FOUND "
                "FALLBACK TO FULL KEY LOAD"
            )

            return self._load_existing_keys_full(
                table=table,
                key_columns=key_columns,
            )


        date_from, date_to = date_range


        date_from_sql = (
            date_from.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )


        date_to_sql = (
            date_to.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )


        # --------------------------------------------------
        # WHERE
        # --------------------------------------------------

        where_conditions: list[str] = []


        where_conditions.append(

            f"{datetime_column} "
            f">= '{date_from_sql}'"

        )


        where_conditions.append(

            f"{datetime_column} "
            f"<= '{date_to_sql}'"

        )


        # --------------------------------------------------
        # OTHER KEY COLUMNS
        #
        # Например:
        #
        # secid + date
        #
        # board + secid + date
        # --------------------------------------------------

        non_datetime_columns = [

            column

            for column in key_columns

            if column != datetime_column

        ]


        for column in non_datetime_columns:

            values = self._get_unique_values(

                rows=rows,

                columns=columns,

                column=column,

            )


            if not values:

                continue


            # --------------------------------------------------
            # ONE VALUE
            # --------------------------------------------------

            if len(values) == 1:

                condition = (

                    f"{column} = "
                    f"{self._format_sql_value(values[0])}"

                )


                where_conditions.append(
                    condition
                )


            # --------------------------------------------------
            # MULTIPLE VALUES
            # --------------------------------------------------

            else:

                formatted_values = [

                    self._format_sql_value(
                        value
                    )

                    for value in values

                ]


                where_conditions.append(

                    f"{column} IN "
                    f"({', '.join(formatted_values)})"

                )


        where_sql = "\n        AND ".join(
            where_conditions
        )


        # --------------------------------------------------
        # SQL
        # --------------------------------------------------

        sql = f"""

        SELECT

            {", ".join(key_columns)}

        FROM {table}

        WHERE {where_sql}

        """


        logger.info(
            "LOAD RANGE EXISTING KEYS TABLE=%s",
            table,
        )


        logger.info(
            "DATE RANGE COLUMN=%s FROM=%s TO=%s",
            datetime_column,
            date_from_sql,
            date_to_sql,
        )


        logger.info(
            "FILTER COLUMNS=%s",
            non_datetime_columns,
        )


        logger.debug(
            "RANGE SQL=%s",
            sql,
        )


        print("=" * 80)
        print("LOAD EXISTING KEYS BY RANGE")
        print("=" * 80)

        print(
            f"TABLE : {table}"
        )

        print(
            f"DATE  : {datetime_column}"
        )

        print(
            f"FROM  : {date_from_sql}"
        )

        print(
            f"TO    : {date_to_sql}"
        )

        print(
            "FILTER:"
        )

        for column in non_datetime_columns:

            values = self._get_unique_values(
                rows=rows,
                columns=columns,
                column=column,
            )

            print(
                f"  {column}: {values}"
            )


        try:

            result = self.client.query(
                sql
            )

        except Exception as error:

            logger.exception(
                "LOAD RANGE EXISTING KEYS ERROR "
                "TABLE=%s ERROR=%s",
                table,
                error,
            )

            raise


        normalized: set[tuple] = set()


        for row in result.result_rows:

            values = list(row)


            for index, column in enumerate(
                key_columns
            ):

                if (
                    column
                    in self.DATETIME_COLUMNS
                ):

                    values[index] = (
                        self._normalize_datetime(
                            values[index]
                        )
                    )


            normalized.add(
                tuple(values)
            )


        logger.info(
            "RANGE EXISTING KEYS LOADED "
            "TABLE=%s COUNT=%s",
            table,
            len(normalized),
        )


        print(
            f"FOUND IN RANGE: {len(normalized)}"
        )


        return normalized


    # ==================================================
    # FULL FALLBACK
    # ==================================================

    def _load_existing_keys_full(
        self,
        table: str,
        key_columns: list[str],
    ) -> set[tuple]:
        """
        Старый режим.

        Используется только если невозможно
        определить datetime-колонку или
        диапазон дат.

        Для больших таблиц такой режим
        крайне нежелателен.
        """

        if not key_columns:
            return set()


        sql = f"""

        SELECT

            {", ".join(key_columns)}

        FROM {table}

        """


        logger.warning(
            "FULL EXISTING KEYS LOAD "
            "TABLE=%s",
            table,
        )


        logger.debug(
            "FULL KEY SQL=%s",
            sql,
        )


        print("=" * 80)
        print("WARNING: LOAD ALL EXISTING KEYS")
        print("=" * 80)

        print(
            f"TABLE: {table}"
        )

        print(
            f"KEYS : {', '.join(key_columns)}"
        )

        print(
            "WARNING: FULL TABLE KEY LOAD"
        )


        try:

            result = self.client.query(
                sql
            )

        except Exception as error:

            logger.exception(
                "LOAD EXISTING KEYS ERROR "
                "TABLE=%s ERROR=%s",
                table,
                error,
            )

            raise


        normalized: set[tuple] = set()


        for row in result.result_rows:

            values = list(row)


            for index, column in enumerate(
                key_columns
            ):

                if (
                    column
                    in self.DATETIME_COLUMNS
                ):

                    values[index] = (
                        self._normalize_datetime(
                            values[index]
                        )
                    )


            normalized.add(
                tuple(values)
            )


        logger.info(
            "EXISTING KEYS LOADED "
            "TABLE=%s COUNT=%s",
            table,
            len(normalized),
        )


        print(
            f"FOUND: {len(normalized)}"
        )


        return normalized


    # ==================================================
    # NORMALIZATION
    # ==================================================

    @classmethod
    def _normalize_value(
        cls,
        column: str,
        value: Any,
    ) -> Any:
        """
        Нормализация значения ключа.
        """

        if column in cls.DATETIME_COLUMNS:

            return cls._normalize_datetime(
                value
            )


        return value


    # ==================================================
    # BUILD KEY
    # ==================================================

    @classmethod
    def _build_key(
        cls,
        row: list[Any],
        columns: list[str],
        key_columns: list[str],
    ) -> tuple:
        """
        Создание составного ключа.
        """

        result = []


        for column in key_columns:

            index = columns.index(
                column
            )


            value = row[index]


            value = cls._normalize_value(
                column,
                value,
            )


            result.append(
                value
            )


        return tuple(result)


    # ==================================================
    # FILTER NEW ROWS
    # ==================================================

    def filter_new_rows(
        self,
        rows: list[list[Any]],
        columns: list[str],
        existing_keys: set[tuple],
        key_columns: list[str],
    ) -> list[list[Any]]:
        """
        Оставляет только новые записи.

        Основной оптимизированный режим:

            текущие строки
                    ↓
            SECID + DATE FROM + DATE TO
                    ↓
            SELECT только этого диапазона
                    ↓
            существующие ключи
                    ↓
            проверка дублей

        Таким образом, Writer никогда
        не загружает 60+ млн ключей
        в память Python.
        """

        logger.info(
            "CHECK DUPLICATES START "
            "INPUT_ROWS=%s",
            len(rows),
        )


        logger.debug(
            "KEY COLUMNS=%s",
            key_columns,
        )


        # ==================================================
        # OPTIMIZED MODE
        # ==================================================

        if isinstance(
            existing_keys,
            _LazyExistingKeys,
        ):

            logger.info(
                "DUPLICATE CHECK MODE="
                "SECID + DATE RANGE"
            )


            print("=" * 80)
            print("CHECK DUPLICATES")
            print("=" * 80)

            print(
                f"INPUT ROWS : {len(rows)}"
            )

            print(
                "MODE       : "
                "SECID + DATE RANGE"
            )


            existing_keys = (
                self._load_existing_keys_for_range(

                    lazy_keys=existing_keys,

                    rows=rows,

                    columns=columns,

                )
            )


        # ==================================================
        # STANDARD MODE
        # ==================================================

        else:

            logger.info(
                "DUPLICATE CHECK MODE=STANDARD"
            )


            print("=" * 80)
            print("CHECK DUPLICATES")
            print("=" * 80)

            print(
                f"INPUT ROWS    : {len(rows)}"
            )

            print(
                f"EXISTING KEYS : "
                f"{len(existing_keys)}"
            )


        # ==================================================
        # INTERNAL DUPLICATE CHECK
        # ==================================================

        result: list[list[Any]] = []

        duplicates = 0


        checked_keys = set(
            existing_keys
        )


        for row in rows:

            key = self._build_key(

                row=row,

                columns=columns,

                key_columns=key_columns,

            )


            # ----------------------------------------------
            # Уже существует в ClickHouse
            # или уже встретился внутри текущего пакета
            # ----------------------------------------------

            if key in checked_keys:

                duplicates += 1

                continue


            result.append(
                row
            )


            checked_keys.add(
                key
            )


        logger.info(
            "CHECK DUPLICATES COMPLETE "
            "INPUT=%s DUPLICATES=%s NEW=%s",
            len(rows),
            duplicates,
            len(result),
        )


        print(
            f"EXISTING KEYS : "
            f"{len(existing_keys)}"
        )

        print(
            f"DUPLICATES    : "
            f"{duplicates}"
        )

        print(
            f"NEW ROWS      : "
            f"{len(result)}"
        )


        return result
