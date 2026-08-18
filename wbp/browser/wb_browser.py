import json
import re
import time

from pathlib import Path

from playwright.sync_api import sync_playwright

from storage.session_manager import SessionManager



class WBBrowser:


    def __init__(
            self,
            session: SessionManager,
            logger
    ):


        self.session = session
        self.logger = logger


        self.profile_dir = (

            Path(__file__)
            .parent
            .parent
            /
            "data"
            /
            "browser_profile"

        )


        self.profile_dir.mkdir(
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

        self.api_found = False





    def start(self):


        self.logger.info(
            "Запуск Chromium"
        )


        try:


            self.playwright = (
                sync_playwright()
                .start()
            )



            self.context = (
                self.playwright
                .chromium
                .launch_persistent_context(

                    user_data_dir=str(
                        self.profile_dir
                    ),


                    headless=False,


                    locale="ru-RU",


                    viewport={

                        "width":1280,

                        "height":900

                    }

                )
            )

            if self.context.pages:
                self.page = self.context.pages[0]
            else:
                self.page = self.context.new_page()

            self.context.on(
                "request",
                lambda request: self.logger.info(
                    "REQUEST: %s",
                    request.url
                )
            )

            self.context.on(
                "response",
                self.response_handler
            )



            self.logger.info(
                "Chromium успешно запущен"
            )



        except Exception as e:


            self.logger.exception(
                "Ошибка запуска Chromium: %s",
                e
            )


            raise

    def response_handler(
            self,
            response
    ):

        try:

            response_url = response.url

            self.logger.info(
                "RESPONSE: %s",
                response_url
            )

            # ==========================
            # SELLER PRODUCTS JSON
            # ==========================

            if "u-card/cards/v4/list" in response_url:

                try:

                    content_type = response.headers.get(
                        "content-type",
                        ""
                    )

                    if "application/json" in content_type:
                        data = response.json()

                        filename = (
                                "seller_catalog_"
                                +
                                str(int(time.time()))
                                +
                                ".json"
                        )

                        path = (
                                Path(__file__)
                                .parent
                                .parent
                                /
                                "data"
                                /
                                "seller_debug"
                        )

                        path.mkdir(
                            parents=True,
                            exist_ok=True
                        )

                        with open(
                                path / filename,
                                "w",
                                encoding="utf-8"
                        ) as f:
                            json.dump(
                                data,
                                f,
                                ensure_ascii=False,
                                indent=2
                            )

                        self.logger.info(
                            "CATALOG JSON сохранен: %s",
                            filename
                        )

                except Exception as e:

                    self.logger.exception(
                        "Ошибка сохранения каталога: %s",
                        e
                    )

            # ==========================
            # PRODUCT API
            # ==========================

            if not self.sku:
                return

            if self.api_found:
                return



            response_url = response.url

            self.logger.info(
                "RESPONSE: %s",
                response_url
            )

            if (
                    "api" in response_url
                    or
                    "catalog" in response_url
                    or
                    "seller" in response_url
            ):
                self.logger.info(
                    "API RESPONSE: %s",
                    response_url
                )

            if (

                "u-card/cards/v4/detail"

                in response_url


                and


                f"nm={self.sku}"

                in response_url

            ):



                self.api_found = True


                self.api_url = response_url



                self.api_headers = dict(

                    response.request.headers

                )



                self.api_method = (

                    response.request.method

                )



                self.logger.info(

                    "Найден API товара SKU %s: %s",

                    self.sku,

                    response_url

                )



                self.session.save_request_data(

                    self.sku,

                    self.api_url,

                    self.api_method

                )



                self.session.save_headers(

                    self.sku,

                    self.api_headers

                )



                self.logger.info(
                    "REQUEST сохранен"
                )


                self.logger.info(
                    "HEADERS сохранены"
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


        try:


            self.logger.info(

                "Открываем товар: %s",

                url

            )



            self.api_url = None

            self.api_headers = {}

            self.api_method = None

            self.api_found = False



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

                "SKU товара: %s",

                self.sku

            )



            self.page.goto(

                url,

                wait_until="commit",

                timeout=60000

            )

            self.logger.info(
                "Короткое ожидание API"
            )

            for _ in range(3):

                if self.api_url:
                    return

                time.sleep(1)


            self.logger.warning(

                "API не найден. Выполняем reload"

            )



            self.page.reload(

                wait_until="commit",

                timeout=60000

            )



            for _ in range(15):


                if self.api_url:


                    return



                time.sleep(1)





            raise Exception(

                "API Wildberries не найден"

            )



        except Exception as e:


            self.logger.exception(

                "Ошибка открытия товара %s: %s",

                url,

                e

            )


            raise








    def get_product(
            self,
            sku=None
    ):


        try:


            if not self.api_url:


                raise Exception(

                    "API URL отсутствует"

                )



            self.logger.info(

                "Получение JSON: %s",

                self.api_url

            )



            headers = {


                key:value


                for key,value


                in self.api_headers.items()



                if key.lower()

                not in [


                    "cookie",

                    "content-length",

                    "host",

                    "origin"

                ]

            }




            result = self.page.evaluate(


                """

                async ({url,headers}) => {


                    const response = await fetch(

                        url,

                        {

                            method:"GET",

                            headers:headers,

                            credentials:"include"

                        }

                    );


                    return {

                        status:response.status,

                        body:await response.text()

                    };


                }

                """,



                {


                    "url":self.api_url,


                    "headers":headers


                }


            )




            self.logger.info(

                "STATUS: %s",

                result["status"]

            )



            if result["status"] != 200:


                raise Exception(

                    f"WB API error {result['status']}"

                )



            data = json.loads(

                result["body"]

            )



            self.session.save_product_response(

                self.sku,

                data

            )



            self.logger.info(

                "RAW JSON сохранен"

            )



            return data





        except Exception as e:


            self.logger.exception(

                "Ошибка получения товара: %s",

                e

            )


            raise

    def save_session(
            self,
            file=None
    ):

        try:

            if file is None:
                file = (
                        self.session.session_dir
                        /
                        "browser_session.json"
                )

            file = Path(file)

            # если передали папку
            if file.suffix == "":
                file = (
                        file
                        /
                        "browser_session.json"
                )

            file.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            data = {

                "cookies": self.context.cookies(),

                "profile_dir": str(
                    self.profile_dir
                )

            }

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
                "Browser session сохранена: %s",
                file
            )


        except Exception as e:

            self.logger.exception(
                "Ошибка сохранения browser session: %s",
                e
            )

            raise




    def close(self):


        self.logger.info(

            "Закрытие браузера"

        )


        try:


            if self.page:

                self.page.close()



            if self.context:

                self.context.close()



            if self.playwright:

                self.playwright.stop()



            self.logger.info(

                "Браузер закрыт"

            )



        except Exception as e:


            self.logger.exception(

                "Ошибка закрытия браузера: %s",

                e

            )