from __future__ import annotations

from typing import Iterable

from client.moex_client import MoexClient
from models.security_search_model import SecuritySearchModel
from utils.iss_parser import IssParser


class SecuritySearchService:

    # Пока проверяем известный валютный рынок.
    # Позже можно добавить stock, futures, bonds и т.д.
    SEARCH_TARGETS = [
        ("currency", "selt"),
    ]

    def __init__(
        self,
        client: MoexClient,
    ) -> None:

        self.client = client

    def search(
        self,
        secid: str,
    ) -> list[SecuritySearchModel]:

        result: list[SecuritySearchModel] = []

        for engine, market in self.SEARCH_TARGETS:

            response = self.client.get(
                f"engines/{engine}/markets/{market}/securities.json"
            )

            securities = IssParser.table(
                response,
                "securities",
            )

            for security in securities:

                if security.get("SECID") != secid:
                    continue

                result.append(
                    SecuritySearchModel(
                        secid=security.get("SECID", ""),
                        shortname=security.get("SHORTNAME", ""),
                        board=security.get("BOARDID", ""),
                        engine=engine,
                        market=market,
                    )
                )

        return result