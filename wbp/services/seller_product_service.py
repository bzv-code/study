import time

from api.wb_client import WBClient

from parser.seller_product_parser import SellerProductParser

from storage.seller_excel_writer import SellerExcelWriter



class SellerProductService:


    def __init__(
            self,
            logger,
            session
    ):

        self.logger = logger

        self.session = session


        self.client = WBClient(
            logger
        )


        self.parser = SellerProductParser(
            logger
        )



    def run(
            self,
            skus
    ):


        products = []


        for index, sku in enumerate(
                skus,
                start=1
        ):


            try:


                start = time.time()


                self.logger.info(
                    "Товар %s/%s SKU %s",
                    index,
                    len(skus),
                    sku
                )


                data = self.client.get_product(
                    sku
                )


                product = self.parser.parse(
                    data,
                    sku
                )


                products.append(
                    product
                )


                self.logger.info(
                    "SKU %s готов %.2f сек",
                    sku,
                    time.time()-start
                )


            except Exception as e:

                self.logger.exception(
                    "Ошибка SKU %s: %s",
                    sku,
                    e
                )



        if products:


            SellerExcelWriter(
                self.session,
                self.logger
            ).save(
                products
            )



        self.client.close()