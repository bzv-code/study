from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class CacheService:

    def __init__(
        self,
        cache_dir: str | Path = "cache",
    ) -> None:

        self.cache_dir = Path(cache_dir)

        self.cache_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    def _file(
        self,
        name: str,
    ) -> Path:

        return self.cache_dir / f"{name}.json"

    def exists(
        self,
        name: str,
    ) -> bool:

        return self._file(name).exists()

    def load(
        self,
        name: str,
    ) -> list[dict[str, Any]]:

        with open(
            self._file(name),
            "r",
            encoding="utf-8",
        ) as fp:

            return json.load(fp)

    def save(
        self,
        name: str,
        data: list[dict[str, Any]],
    ) -> None:

        with open(
            self._file(name),
            "w",
            encoding="utf-8",
        ) as fp:

            json.dump(
                data,
                fp,
                ensure_ascii=False,
                indent=4,
            )