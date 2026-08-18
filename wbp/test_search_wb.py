import json
from pathlib import Path
from urllib.parse import urlparse, parse_qs

from playwright.sync_api import Response


class SearchDebug:

    def __init__(
            self,
            browser,
            logger,
            project_path
    ):

        self.browser = browser
        self.logger = logger

        self.path = (
            Path(project_path)
            / "search_debug"
        )

        self.path.mkdir(
            parents=True,
            exist_ok=True
        )

        self.saved = set()
        self.counter = {}

    def attach(self):

        self.logger.info(
            "SearchDebug подключен"
        )

        self.browser.page.on(
            "response",
            self.response_handler
        )

    def response_handler(
            self,
            response: Response
    ):

        try:

            url = response.url

            # Интересуют только запросы поиска WB
            if "/__internal/u-search/" not in url:
                return

            if url in self.saved:
                return

            self.saved.add(url)

            self.logger.info("=" * 100)
            self.logger.info("U-SEARCH RESPONSE")
            self.logger.info(url)

            content_type = response.headers.get(
                "content-type",
                ""
            )

            if "json" not in content_type.lower():
                self.logger.info(
                    "Не JSON (%s)",
                    content_type
                )
                return

            try:
                data = response.json()

            except Exception as e:

                self.logger.warning(
                    "Не удалось получить JSON: %s",
                    e
                )

                return

            params = parse_qs(
                urlparse(url).query
            )

            resultset = params.get(
                "resultset",
                ["unknown"]
            )[0]

            self.counter[resultset] = (
                self.counter.get(resultset, 0) + 1
            )

            filename = (
                f"u-search_{resultset}_{self.counter[resultset]:03d}.json"
            )

            filepath = self.path / filename

            with open(
                    filepath,
                    "w",
                    encoding="utf-8"
            ) as f:

                json.dump(
                    data,
                    f,
                    ensure_ascii=False,
                    indent=4
                )

            self.logger.info(
                "JSON сохранен: %s",
                filename
            )

        except Exception as e:

            self.logger.exception(
                "Ошибка SearchDebug: %s",
                e
            )