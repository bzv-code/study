import time

from parser.product_parser import ProductParser
from storage.excel_writer import ExcelWriter

from api.wb_client import WBClient
from storage.session_manager import SessionManager


class APIProductService:


    def __init__(
            self,
            logger
    ):

        self.logger = logger


        self.session = SessionManager(
            logger
        )


        self.client = WBClient(
            logger
        )


        self.parser = ProductParser(

            self.session,

            logger

        )



    def run(
            self,
            skus
    ):


        results = []


        success = 0

        failed = 0



        self.logger.info(
            "Запуск APIProductService"
        )


        self.logger.info(
            "Количество товаров: %s",
            len(skus)
        )



        try:


            for index, sku in enumerate(
                    skus,
                    start=1
            ):


                self.logger.info(
                    "=========================="
                )


                self.logger.info(
                    "Товар %s/%s",
                    index,
                    len(skus)
                )



                start = time.time()



                try:


                    data = self.client.get_product(
                        sku
                    )



                    product = self.parser.parse_json(

                        data,

                        f"https://www.wildberries.ru/catalog/{sku}/detail.aspx"

                    )



                    results.append(
                        product
                    )


                    success += 1



                    self.logger.info(

                        "SKU %s обработан за %.2f сек",

                        sku,

                        time.time() - start

                    )



                except Exception as e:


                    failed += 1


                    self.logger.exception(

                        "Ошибка SKU %s: %s",

                        sku,

                        e

                    )





            if results:

                ExcelWriter(

                    self.session,

                    self.logger

                ).save(

                    results

                )



        finally:



            summary = {


                "total": len(skus),


                "success": success,


                "failed": failed


            }



            self.logger.info(
                "ИТОГО: %s",
                summary
            )



            self.client.close()



            self.logger.info(
                "API режим завершен"
            )