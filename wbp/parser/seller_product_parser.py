from datetime import datetime

from models.seller_product import SellerProduct



class SellerProductParser:


    def __init__(
            self,
            logger
    ):

        self.logger = logger



    def parse(
            self,
            data,
            sku
    ):


        products = data.get(
            "products",
            []
        )


        if not products:

            raise Exception(
                "Нет products"
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
                /
                100
            )


            price_old = (
                price_data.get(
                    "basic",
                    0
                )
                /
                100
            )



        return SellerProduct(


            parse_date=datetime.now(),


            title=product.get(
                "name"
            ),


            brand=product.get(
                "brand"
            ),


            supplier=product.get(
                "supplier"
            ),


            sku=sku,


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


            url=
            f"https://www.wildberries.ru/catalog/{sku}/detail.aspx",


            seller_url=
            "https://www.wildberries.ru/seller/4032338"

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

                if isinstance(
                        data["price"],
                        dict
                ):

                    if data["price"].get(
                            "product"
                    ):

                        return data["price"]



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