import re

from datetime import datetime

from models.search_product import SearchProduct



class SearchProductParser:


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
                "Парсинг поискового товара SKU: %s",
                product_id
            )



            products = data.get(
                "products",
                []
            )



            if not products:


                raise Exception(
                    "В JSON отсутствует products"
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



            supplier = product.get(
                "supplier"
            )



            supplier_id = product.get(
                "supplierId"
            )



            shop_url = None



            if supplier_id:


                shop_url = (
                    "https://www.wildberries.ru/seller/"
                    +
                    str(
                        supplier_id
                    )
                )



            result = SearchProduct(


                parse_date=datetime.now(),


                title=product.get(
                    "name"
                ),


                brand=product.get(
                    "brand"
                ),


                supplier=supplier,


                sku=product.get(
                    "id"
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


                price=price,


                url=url,


                shop_url=shop_url

            )



            self.logger.info(
                "Поисковый товар обработан: %s",
                result.title
            )


            return result



        except Exception as e:


            self.logger.exception(
                "Ошибка SearchProductParser %s: %s",
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