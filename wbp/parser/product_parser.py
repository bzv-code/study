import re

from datetime import datetime

from models.product import Product


class ProductParser:


    def __init__(
            self,
            session,
            logger
    ):

        self.session = session
        self.logger = logger



    def parse_json(
            self,
            data,
            url
    ):


        try:


            product_id = self.extract_id(
                url
            )


            self.logger.info(
                "Парсинг SKU: %s",
                product_id
            )



            products = data.get(
                "products",
                []
            )



            if not products:


                self.logger.error(
                    "В JSON отсутствует products. SKU: %s",
                    product_id
                )


                raise Exception(
                    "В JSON нет products"
                )



            product = products[0]



            price = 0
            price_old = 0



            price_data = self.find_price(
                data
            )



            if price_data:


                price = (

                    price_data.get(
                        "product",
                        0
                    )

                    / 100

                )



                price_old = (

                    price_data.get(
                        "basic",
                        0
                    )

                    / 100

                )


                self.logger.info(
                    "Цена найдена SKU %s: %s",
                    product_id,
                    price_data
                )



            else:


                self.logger.warning(
                    "Цена не найдена SKU: %s",
                    product_id
                )



            result = Product(


                parse_date=datetime.now(),


                url=url,


                sku=product.get(
                    "id"
                ),


                title=product.get(
                    "name"
                ),


                brand=product.get(
                    "brand"
                ),


                supplier=product.get(
                    "supplier"
                ),


                sku_rating=product.get(
                    "nmReviewRating",
                    0
                ),


                sku_reviews_count=product.get(
                    "nmFeedbacks",
                    0
                ),


                price_old=price_old,


                price=price

            )



            self.logger.info(
                "Товар обработан: %s",
                result.title
            )


            self.logger.info(
                "Цена товара: %s",
                result.price
            )



            return result



        except Exception as e:


            self.logger.exception(
                "Ошибка парсинга товара %s: %s",
                url,
                e
            )


            raise





    @staticmethod
    def extract_id(
            url
    ):


        result = re.search(
            r"catalog/(\d+)",
            url
        )


        if result:

            return int(
                result.group(1)
            )



        result = re.search(
            r"nm=(\d+)",
            url
        )


        if result:

            return int(
                result.group(1)
            )



        raise ValueError(
            f"SKU не найден: {url}"
        )





    def find_price(
            self,
            data
    ):


        if isinstance(
                data,
                dict
        ):


            if "price" in data:


                price = data["price"]


                if isinstance(
                        price,
                        dict
                ):


                    if price.get(
                            "product"
                    ):

                        return price



            for value in data.values():


                result = self.find_price(
                    value
                )


                if result:

                    return result





        elif isinstance(
                data,
                list
        ):


            for item in data:


                result = self.find_price(
                    item
                )


                if result:

                    return result



        return None