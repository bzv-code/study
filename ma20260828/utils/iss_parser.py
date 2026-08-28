from __future__ import annotations

from typing import Any


class IssParser:
    """
    Универсальный парсер ответов ISS API MOEX.

    ISS возвращает данные в формате:

    {
        "table_name": {
            "columns": [],
            "data": []
        }
    }
    """

    @staticmethod
    def table(
            response: dict[str, Any],
            table_name: str,
    ) -> list[dict[str, Any]]:
        """
        Преобразует таблицу ISS в список словарей.
        """

        table = response.get(table_name)

        if table is None:
            return []

        columns = table.get(
            "columns",
            []
        )

        rows = table.get(
            "data",
            []
        )

        return [
            dict(zip(columns, row))
            for row in rows
        ]

    @staticmethod
    def first(
            response: dict[str, Any],
            table_name: str,
    ) -> dict[str, Any] | None:
        """
        Возвращает первую запись таблицы.
        """

        rows = IssParser.table(
            response,
            table_name,
        )

        if not rows:
            return None

        return rows[0]