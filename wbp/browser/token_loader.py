import json
import re
import time

from pathlib import Path

from playwright.sync_api import sync_playwright

from storage.session_manager import SessionManager



class WBTokenLoader:


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


        self.playwright = None
        self.context = None
        self.page = None


        self.api_url = None
        self.api_headers = {}

        self.sku = None



    def load(
            self,
            url
    ):


        self.logger.info(
            "Запуск Token Loader"
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


        self.page = self.context.new_page()



        match = re.search(
            r"catalog/(\d+)",
            url
        )


        if not match:


            raise Exception(
                "SKU не найден"
            )



        self.sku = match.group(1)



        self.page.on(
            "response",
            self.response_handler
        )



        self.logger.info(
            "Открываем товар: %s",
            url
        )



        self.page.goto(

            url,

            wait_until="commit",

            timeout=60000

        )



        self.wait_api()



        cookies = self.context.cookies()



        token = None



        for cookie in cookies:


            if cookie["name"] == "x_wbaas_token":

                token = cookie["value"]



        user_agent = self.page.evaluate(

            "() => navigator.userAgent"

        )



        self.save_session_data(

            token,

            cookies,

            user_agent

        )



        self.logger.info(
            "Token получен: %s",
            bool(token)
        )



        return {


            "page": self.page,

            "api_url": self.api_url,

            "api_headers": self.api_headers,

            "token": token

        }




    def response_handler(
            self,
            response
    ):


        try:


            if self.api_url:

                return



            response_url = response.url



            if (

                "u-card/cards/v4/detail"
                in response_url

                and

                f"nm={self.sku}"
                in response_url

            ):



                self.api_url = response_url



                self.api_headers = dict(

                    response.request.headers

                )



                self.session.save_request_data(

                    self.sku,

                    self.api_url,

                    response.request.method

                )



                self.session.save_headers(

                    self.sku,

                    self.api_headers

                )



                self.logger.info(
                    "API найден: %s",
                    response_url
                )



        except Exception as e:


            self.logger.exception(
                "Ошибка обработки response: %s",
                e
            )





    def wait_api(self):


        self.logger.info(
            "Ожидание API..."
        )


        for _ in range(15):


            if self.api_url:

                return


            time.sleep(1)



        self.logger.warning(
            "API не найден, reload"
        )



        self.page.reload(

            wait_until="commit",

            timeout=60000

        )



        for _ in range(30):


            if self.api_url:

                return


            time.sleep(1)



        raise Exception(
            "API WB не найден"
        )





    def save_session_data(
            self,
            token,
            cookies,
            user_agent
    ):



        file = (

            self.session.session_dir
            /
            "token.json"

        )



        data = {


            "token": token,

            "user_agent": user_agent,

            "cookies": cookies


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
            "Token данные сохранены: %s",
            file
        )





    def close(self):


        if self.context:

            self.context.close()



        if self.playwright:

            self.playwright.stop()



        self.logger.info(
            "Token Loader закрыт"
        )