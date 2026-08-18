import json

import httpx

from pathlib import Path
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse



class WBClient:


    def __init__(
            self,
            logger
    ):

        self.logger = logger


        self.session_dir = (

            Path(__file__)
            .parent
            .parent
            /
            "data"
            /
            "browser_session"

        )


        self.api_url = None

        self.headers = {}

        self.cookies = {}


        self.client = None



        self.load_session()

        self.create_client()



    def load_session(self):


        self.logger.info(
            "Загрузка Browser Session"
        )


        api_file = (
            self.session_dir
            /
            "api.json"
        )


        headers_file = (
            self.session_dir
            /
            "headers.json"
        )


        cookies_file = (
            self.session_dir
            /
            "cookies.json"
        )



        files = [

            api_file,

            headers_file,

            cookies_file

        ]



        for file in files:


            if not file.exists():


                raise FileNotFoundError(

                    f"Не найден файл Browser Session: {file}"

                )



        with open(
                api_file,
                encoding="utf-8"
        ) as f:


            api = json.load(f)



        self.api_url = api["url"]




        with open(
                headers_file,
                encoding="utf-8"
        ) as f:


            self.headers = json.load(f)




        with open(
                cookies_file,
                encoding="utf-8"
        ) as f:


            cookies = json.load(f)



        self.cookies = {


            item["name"]:
            item["value"]


            for item in cookies

        }



        self.logger.info(
            "Session загружена"
        )


        self.logger.info(
            "Cookies: %s",
            len(self.cookies)
        )


        self.logger.info(
            "Headers: %s",
            len(self.headers)
        )





    def create_client(self):


        self.client = httpx.Client(


            headers=self.prepare_headers(),


            cookies=self.cookies,


            timeout=httpx.Timeout(
                30.0
            ),


            follow_redirects=True


        )



        self.logger.info(
            "HTTPX клиент создан"
        )





    def get_product(
            self,
            sku:int
    ):


        url = self.build_url(
            sku
        )


        self.logger.info(
            "Запрос WB API SKU %s",
            sku
        )



        try:


            response = self.client.get(
                url
            )



            self.logger.info(
                "STATUS SKU %s: %s",
                sku,
                response.status_code
            )



            if response.status_code != 200:


                raise Exception(

                    f"WB API error {response.status_code}"

                )



            return response.json()



        except Exception as e:


            self.logger.exception(

                "Ошибка WB API SKU %s: %s",

                sku,

                e

            )


            raise





    def build_url(
            self,
            sku:int
    ):


        parsed = urlparse(
            self.api_url
        )


        query = parse_qs(
            parsed.query
        )



        query["nm"] = [
            str(sku)
        ]



        new_query = urlencode(

            query,

            doseq=True

        )



        return urlunparse(

            (

                parsed.scheme,

                parsed.netloc,

                parsed.path,

                parsed.params,

                new_query,

                parsed.fragment

            )

        )





    def prepare_headers(self):


        remove = [

            "content-length",

            "host",

            "origin"

        ]



        return {


            key:value


            for key,value in self.headers.items()


            if key.lower()

            not in remove

        }





    def close(self):


        if self.client:


            self.client.close()


            self.logger.info(
                "HTTPX клиент закрыт"
            )