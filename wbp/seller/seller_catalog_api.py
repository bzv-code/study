import httpx


class SellerCatalogAPI:


    URL = (
        "https://www.wildberries.ru/"
        "__internal/u-catalog/sellers/v4/catalog"
    )


    def __init__(
            self,
            logger
    ):

        self.logger = logger



    def get_catalog(
            self,
            seller_id
    ):


        params = {

            "ab_testid": "new_cb_1",

            "appType": 1,

            "curr": "rub",

            "dest": -1257786,

            "hide_dtype": 15,

            "hide_vflags": 4294967296,

            "lang": "ru",

            "page": 1,

            "sort": "popular",

            "spp": 30,

            "supplier": seller_id

        }



        headers = {

            "User-Agent":
            "Mozilla/5.0"

        }



        self.logger.info(
            "Запрос каталога продавца API"
        )



        with httpx.Client(
                headers=headers,
                timeout=30
        ) as client:


            response = client.get(
                self.URL,
                params=params
            )



            response.raise_for_status()



            data = response.json()



        self.logger.info(
            "Каталог получен"
        )


        return data