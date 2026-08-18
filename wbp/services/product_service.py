import time


from services.base_service import BaseService

from parser.product_parser import ProductParser
from storage.excel_writer import ExcelWriter





class ProductService(BaseService):


    def __init__(
            self,
            logger
    ):

        super().__init__(
            logger
        )


        self.parser = ProductParser(
            self.session,
            self.logger
        )





    def run(
            self,
            urls
    ):


        results = []


        success = 0

        failed = 0


        product_stats = []



        self.logger.info(
            "Запуск ProductService"
        )


        self.logger.info(
            "Количество товаров для обработки: %s",
            len(urls)
        )



        try:


            self.start()



            for index, url in enumerate(
                    urls,
                    start=1
            ):


                start_time = time.time()


                sku = None



                self.logger.info(
                    "=========================="
                )


                self.logger.info(
                    "Обработка товара %s/%s",
                    index,
                    len(urls)
                )


                self.logger.info(
                    "URL: %s",
                    url
                )



                try:


                    self.browser.open_product(
                        url
                    )


                    sku = self.browser.sku



                    data = self.browser.get_product()



                    product = self.parser.parse_json(
                        data,
                        url
                    )



                    results.append(
                        product
                    )


                    success += 1



                    elapsed = round(
                        time.time() - start_time,
                        2
                    )



                    product_stats.append({

                        "sku": product.sku,

                        "title": product.title,

                        "time_seconds": elapsed,

                        "status": "success"

                    })



                    self.logger.info(
                        "Товар успешно обработан. SKU: %s",
                        product.sku
                    )


                    self.logger.info(
                        "Время обработки SKU %s: %s сек",
                        product.sku,
                        elapsed
                    )



                except Exception as e:


                    failed += 1



                    elapsed = round(
                        time.time() - start_time,
                        2
                    )



                    product_stats.append({

                        "sku": sku,

                        "url": url,

                        "time_seconds": elapsed,

                        "status": "failed",

                        "error": str(e)

                    })



                    self.logger.exception(
                        "Ошибка обработки товара %s: %s",
                        url,
                        e
                    )





            if results:


                self.logger.info(
                    "Сохранение Excel"
                )


                ExcelWriter(
                    self.session,
                    self.logger
                ).save(
                    results
                )


                self.logger.info(
                    "Excel сохранен. Товаров: %s",
                    len(results)
                )



            else:


                self.logger.warning(
                    "Нет данных для сохранения Excel"
                )



        except Exception as e:


            self.logger.exception(
                "Критическая ошибка ProductService: %s",
                e
            )


            raise



        finally:



            summary = {


                "total": len(urls),


                "success": success,


                "failed": failed,


                "products": product_stats


            }



            self.session.save_summary(
                summary
            )



            self.stop()



            self.logger.info(
                "=========================="
            )


            self.logger.info(
                "ProductService завершил работу"
            )


            self.logger.info(
                "Успешно: %s | Ошибок: %s",
                success,
                failed
            )