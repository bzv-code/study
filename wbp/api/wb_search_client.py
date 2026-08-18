import json
from pathlib import Path
from datetime import datetime

import httpx



class WBSearchClient:


    def __init__(
            self,
            logger,
            project_path
    ):

        self.logger = logger

        self.project_path = Path(
            project_path
        )


        self.raw_dir = (
            self.project_path
            /
            "data"
            /
            "search_debug"
            /
            "raw"
        )


        self.raw_dir.mkdir(
            parents=True,
            exist_ok=True
        )


        self.headers = {

            "User-Agent":
            (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/120 Safari/537.36"
            ),


            "Accept":
            "application/json, text/plain, */*",


            "Accept-Language":
            "ru-RU,ru;q=0.9"

        }



    def search(
            self,
            query
    ):


        url = (
            "https://www.wildberries.ru"
            "/__internal/u-search/exactmatch/"
            "ru/common/v18/search"
        )



        params = {


            "ab_testing":
            "false",


            "appType":
            1,


            "curr":
            "rub",


            "dest":
            -1257786,


            "hide_dtype":
            15,


            "hide_vflags":
            4294967296,


            "inheritFilters":
            "true",


            "lang":
            "ru",


            "locale":
            "ru",


            "query":
            query,


            "resultset":
            "catalog",


            "sort":
            "popular",


            "spp":
            30,


            "suppressSpellcheck":
            "false"

        }



        self.logger.info(
            "Запрос WB Search API: %s",
            query
        )



        response = httpx.get(

            url,

            params=params,

            headers=self.headers,

            timeout=30

        )



        self.logger.info(
            "STATUS WB SEARCH: %s",
            response.status_code
        )



        response.raise_for_status()



        data = response.json()



        self.save_raw(
            query,
            data
        )



        return data




    def save_raw(
            self,
            query,
            data
    ):


        filename = (

            "search_"

            +

            datetime.now()
            .strftime(
                "%Y-%m-%d_%H-%M-%S"
            )

            +

            ".json"

        )


        file = (
            self.raw_dir
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
            "RAW JSON сохранен: %s",
            file
        )