import time


from api.wb_client import WBClient

from parser.search_product_parser import SearchProductParser

from storage.session_manager import SessionManager

from storage.search_excel_writer import SearchExcelWriter




class SearchProductService:



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



        self.parser = SearchProductParser(

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
            "Запуск SearchProductService"
        )



        self.logger.info(
            "Количество SKU: %s",
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
                    "Товар %s/%s SKU=%s",
                    index,
                    len(skus),
                    sku
                )



                start = time.time()



                try:



                    data = self.client.get_product(
                        sku
                    )



                    url = (

                        "https://www.wildberries.ru/catalog/"
                        +
                        str(sku)
                        +
                        "/detail.aspx"

                    )



                    product = self.parser.parse_json(

                        data,

                        url

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



                writer = SearchExcelWriter(

                    self.session,

                    self.logger

                )



                writer.save(
                    results
                )




        finally:



            summary = {


                "total": len(skus),


                "success": success,


                "failed": failed


            }



            self.logger.info(
                "ИТОГО SEARCH: %s",
                summary
            )



            self.client.close()



            self.logger.info(
                "SearchProductService завершен"
            )



        return results