import json
import time
import hashlib

from pathlib import Path



class SellerDebug:


    def __init__(
            self,
            browser,
            logger,
            output_path
    ):

        self.browser = browser
        self.logger = logger


        self.output = Path(
            output_path
        )


        self.output.mkdir(
            parents=True,
            exist_ok=True
        )


        self.responses_file = (
            self.output / "responses.jsonl"
        )


        self.last_catalog_hash = None


        self.saved_hashes = set()


        self.counter = 0



    def attach(self):


        self.browser.page.on(
            "response",
            self.handle_response
        )


        self.logger.info(
            "SellerDebug включен"
        )



    # =====================================================
    # Общий лог response
    # =====================================================


    def save_response_log(
            self,
            url,
            data
    ):


        record = {

            "time": time.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            "url": url,

            "data": data

        }



        with open(

                self.responses_file,

                "a",

                encoding="utf-8"

        ) as f:


            f.write(

                json.dumps(

                    record,

                    ensure_ascii=False

                )

                + "\n"

            )




    # =====================================================
    # Сохранение JSON файлов
    # =====================================================


    def save_json(
            self,
            filename,
            url,
            data
    ):


        file = (
            self.output / filename
        )


        with open(

                file,

                "w",

                encoding="utf-8"

        ) as f:


            json.dump(

                {
                    "url": url,
                    "data": data
                },

                f,

                ensure_ascii=False,

                indent=4

            )



        self.logger.info(

            "Сохранен JSON: %s",

            filename

        )



    # =====================================================
    # SKU продавца
    # =====================================================


    def save_catalog_sku(
            self,
            data
    ):


        products = data.get(
            "products",
            []
        )



        if not products:


            self.logger.warning(
                "Каталог пустой"
            )

            return



        sku_list = []



        for product in products:


            sku = product.get(
                "id"
            )



            if not sku:

                continue



            sku_list.append(

                {
                    "id": sku,

                    "name": product.get(
                        "name"
                    ),

                    "brand": product.get(
                        "brand"
                    )

                }

            )




        if not sku_list:


            self.logger.warning(
                "SKU не найдены"
            )

            return



        filename = (

            f"seller_sku_{int(time.time()*1000)}.json"

        )



        file = (

            self.output / filename

        )



        with open(

                file,

                "w",

                encoding="utf-8"

        ) as f:


            json.dump(

                sku_list,

                f,

                ensure_ascii=False,

                indent=4

            )



        self.logger.info(

            "SKU сохранены: %s шт. -> %s",

            len(sku_list),

            filename

        )



    # =====================================================
    # Хеш каталога
    # =====================================================


    def get_catalog_hash(
            self,
            data
    ):


        products = data.get(
            "products",
            []
        )



        return hashlib.md5(

            json.dumps(

                products,

                ensure_ascii=False,

                sort_keys=True

            ).encode()

        ).hexdigest()




    # =====================================================
    # Playwright response handler
    # =====================================================


    def handle_response(
            self,
            response
    ):


        try:


            url = response.url



            content_type = response.headers.get(

                "content-type",

                ""

            )



            if (

                "json" not in content_type

                and

                "javascript" not in content_type

            ):

                return



            if response.status != 200:

                return



            try:

                data = response.json()


            except Exception:

                return




            self.counter += 1



            self.save_response_log(

                url,

                data

            )



            timestamp = int(

                time.time()*1000

            )



            # ============================================
            # Каталог продавца
            # ============================================


            if "u-catalog/sellers/v4/catalog" in url:



                catalog_hash = self.get_catalog_hash(

                    data

                )



                if catalog_hash == self.last_catalog_hash:


                    return



                self.last_catalog_hash = catalog_hash



                self.save_json(

                    f"seller_catalog_{timestamp}.json",

                    url,

                    data

                )



                self.save_catalog_sku(

                    data

                )


                return




            # ============================================
            # Seller API
            # ============================================


            if "u-catalog/sellers" in url:



                filename = (

                    f"seller_filters_{timestamp}.json"

                    if "/filters" in url

                    else

                    f"seller_api_{timestamp}.json"

                )



                self.save_json(

                    filename,

                    url,

                    data

                )


                return




            # ============================================
            # Карточки
            # ============================================


            mapping = {


                "u-card/cards/v4/list":

                    "cards_list",


                "u-card/cards/v4/detail":

                    "card_detail",


                "banners":

                    "banners",


                "frontend-analytics":

                    "frontend_analytics"

            }



            for key, name in mapping.items():


                if key in url:


                    self.save_json(

                        f"{name}_{timestamp}.json",

                        url,

                        data

                    )


                    return



        except Exception as e:


            self.logger.exception(

                "Ошибка обработки response: %s",

                e

            )