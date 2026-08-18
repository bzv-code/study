import json
import re

from pathlib import Path

from playwright.sync_api import sync_playwright


class BrowserSession:


    def __init__(
            self,
            logger
    ):

        self.logger = logger


        self.base_dir = (

            Path(__file__)
            .parent
            .parent
            /
            "data"
            /
            "browser_session"

        )


        self.base_dir.mkdir(
            parents=True,
            exist_ok=True
        )


        self.playwright = None
        self.context = None
        self.page = None


        self.sku = None


        self.api_url = None
        self.api_headers = {}

        self.api_method = None



    def start(self):


        self.logger.info(
            "Запуск BrowserSession"
        )


        self.playwright = (
            sync_playwright()
            .start()
        )


        self.context = (

            self.playwright
            .chromium
            .launch_persistent_context(

                user_data_dir=str(
                    self.base_dir / "profile"
                ),

                headless=False,

                locale="ru-RU",

                viewport={

                    "width":1280,

                    "height":900

                }

            )

        )


        self.page = (
            self.context.new_page()
        )


        self.page.on(
            "response",
            self.response_handler
        )


        self.logger.info(
            "BrowserSession запущен"
        )



    def response_handler(
            self,
            response
    ):


        try:


            if self.api_url:

                return



            url = response.url



            if (

                "u-card/cards/v4/detail"

                in url

            ):


                self.api_url = url


                self.api_method = (
                    response.request.method
                )


                self.api_headers = dict(
                    response.request.headers
                )


                self.logger.info(
                    "Найден WB API"
                )


                self.logger.info(
                    "%s",
                    url
                )



        except Exception as e:


            self.logger.exception(
                "Ошибка обработки response: %s",
                e
            )



    def open_product(
            self,
            url
    ):


        result = re.search(
            r"catalog/(\d+)",
            url
        )


        if not result:

            raise Exception(
                "SKU не найден"
            )


        self.sku = result.group(1)


        self.logger.info(
            "Открываем товар SKU %s",
            self.sku
        )



        self.page.goto(

            url,

            wait_until="commit",

            timeout=60000

        )



        self.page.wait_for_timeout(
            5000
        )



        if not self.api_url:


            self.logger.warning(
                "API не найден, reload"
            )


            self.page.reload(

                wait_until="commit",

                timeout=60000

            )


            self.page.wait_for_timeout(
                5000
            )



        if not self.api_url:

            raise Exception(
                "API WB не найден"
            )




    def save(self):


        cookies = (
            self.context.cookies()
        )


        self._save_json(

            "cookies.json",

            cookies

        )


        self._save_json(

            "headers.json",

            self.api_headers

        )


        self._save_json(

            "api.json",

            {

                "url": self.api_url,

                "method": self.api_method,

                "sku": self.sku

            }

        )



        self.logger.info(
            "Browser session сохранена"
        )




    def _save_json(
            self,
            filename,
            data
    ):


        path = (

            self.base_dir
            /
            filename

        )


        with open(

            path,

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
            "Сохранено: %s",
            path
        )




    def close(self):


        self.logger.info(
            "Закрытие BrowserSession"
        )


        if self.context:

            self.context.close()



        if self.playwright:

            self.playwright.stop()