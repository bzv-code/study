import json
import time

from pathlib import Path
from urllib.parse import urlparse


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
            /
            "search_debug"
        )

        self.path.mkdir(
            parents=True,
            exist_ok=True
        )


        self.counter = 0



    def attach(self):

        self.logger.info(
            "Подключение SearchDebug"
        )


        self.browser.page.on(
            "response",
            self.response_handler
        )



    def response_handler(
            self,
            response
    ):


        try:


            url = response.url



            # Берем только внутренний поиск WB

            if (
                "/__internal/u-search/"
                not in url
            ):
                return



            self.logger.info(
                "U-SEARCH RESPONSE:"
            )

            self.logger.info(
                url
            )



            try:

                body = response.body()


            except Exception as e:

                self.logger.warning(
                    "Не удалось получить body: %s",
                    e
                )

                return



            if not body:

                return



            # пробуем JSON

            try:

                data = json.loads(
                    body.decode(
                        "utf-8"
                    )
                )


            except Exception:


                self.logger.info(
                    "Ответ не JSON"
                )

                return



            # ищем товары

            products = data.get(
                "products"
            )


            if isinstance(
                    products,
                    list
            ):


                self.logger.info(
                    "НАЙДЕН JSON С PRODUCTS"
                )


                self.logger.info(
                    "Количество товаров: %s",
                    len(products)
                )



                filename = (
                    "search_catalog_"
                    +
                    str(
                        int(
                            time.time()
                        )
                    )
                    +
                    ".json"
                )



                file = (
                    self.path
                    /
                    filename
                )



                with open(
                        file,
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
                    "СОХРАНЕНО: %s",
                    file
                )



            else:


                # сохраняем только информацию
                # чтобы понять структуру

                self.counter += 1


                if self.counter <= 10:


                    filename = (
                        "debug_"
                        +
                        str(self.counter)
                        +
                        ".json"
                    )


                    file = (
                        self.path
                        /
                        filename
                    )


                    with open(
                            file,
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
                        "Сохранен DEBUG JSON: %s",
                        file
                    )



        except Exception as e:


            self.logger.exception(
                "Ошибка SearchDebug: %s",
                e
            )