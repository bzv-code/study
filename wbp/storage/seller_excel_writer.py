from openpyxl import Workbook



class SellerExcelWriter:


    def __init__(
            self,
            session,
            logger
    ):


        self.session = session

        self.logger = logger



    def save(
            self,
            products
    ):


        file = (
            self.session.session_dir
            /
            "seller_products.xlsx"
        )


        self.logger.info(
            "Создание Excel: %s",
            file
        )


        wb = Workbook()


        ws = wb.active

        ws.title = "Products"



        ws.append([

            "Дата",
            "Название",
            "Бренд",
            "Поставщик",
            "SKU",
            "Рейтинг",
            "Отзывы",
            "Старая цена",
            "Цена",
            "URL",
            "Магазин"

        ])



        for product in products:


            ws.append([


                product.parse_date,

                product.title,

                product.brand,

                product.supplier,

                product.sku,

                product.sku_rating,

                product.sku_reviews_count,

                product.price_old,

                product.price,

                product.url,

                product.seller_url


            ])



        wb.save(
            file
        )


        self.logger.info(
            "Excel сохранен"
        )