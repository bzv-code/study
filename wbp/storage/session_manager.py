
import json

from datetime import datetime
from pathlib import Path



class SessionManager:


    def __init__(
            self,
            logger
    ):

        self.logger = logger


        # Корень проекта wb_parser
        self.project_path = (
            Path(__file__)
            .parent
            .parent
        )


        self.root = (
            self.project_path
            /
            "data"
            /
            "sessions"
        )


        self.session_name = datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S"
        )


        self.session_dir = (
            self.root
            /
            self.session_name
        )


        self.products_dir = (
            self.session_dir
            /
            "products"
        )


        self.session_dir.mkdir(
            parents=True,
            exist_ok=True
        )


        self.products_dir.mkdir(
            parents=True,
            exist_ok=True
        )


        self.logger.info(
            "Создана директория сессии: %s",
            self.session_dir
        )





    @property
    def excel_file(self):

        return (
            self.session_dir
            /
            "seller_products.xlsx"
        )





    @property
    def seller_catalog_file(self):

        return (
            self.session_dir
            /
            "seller_catalog.json"
        )





    @property
    def seller_sku_file(self):

        return (
            self.session_dir
            /
            "seller_sku.json"
        )





    def product_dir(
            self,
            sku
    ):


        path = (
            self.products_dir
            /
            str(sku)
        )


        path.mkdir(
            parents=True,
            exist_ok=True
        )


        return path





    def response_file(
            self,
            sku
    ):


        return (
            self.product_dir(sku)
            /
            "response.json"
        )





    def request_file(
            self,
            sku
    ):


        return (
            self.product_dir(sku)
            /
            "request.json"
        )





    def headers_file(
            self,
            sku
    ):


        return (
            self.product_dir(sku)
            /
            "headers.json"
        )





    def product_file(
            self,
            sku
    ):


        return (
            self.product_dir(sku)
            /
            "product.json"
        )





    def summary_file(self):

        return (
            self.session_dir
            /
            "summary.json"
        )





    def log_file(self):

        return (
            self.session_dir
            /
            "parser.log"
        )





    def save_json(
            self,
            file,
            data
    ):

        try:


            file = Path(file)


            file.parent.mkdir(
                parents=True,
                exist_ok=True
            )


            with open(
                    file,
                    "w",
                    encoding="utf-8"
            ) as f:


                json.dump(
                    data,
                    f,
                    ensure_ascii=False,
                    indent=4
                )



            self.logger.info(
                "JSON сохранен: %s",
                file
            )



        except Exception as e:


            self.logger.exception(
                "Ошибка сохранения JSON %s: %s",
                file,
                e
            )

            raise





    # ============================
    # REQUEST / HEADERS / RESPONSE
    # ============================


    def save_request_data(
            self,
            sku,
            url,
            method
    ):


        data = {

            "sku": sku,

            "url": url,

            "method": method

        }


        self.save_json(

            self.request_file(sku),

            data

        )





    def save_headers(
            self,
            sku,
            headers
    ):


        self.save_json(

            self.headers_file(sku),

            headers

        )





    def save_product_response(
            self,
            sku,
            data
    ):


        self.save_json(

            self.response_file(sku),

            data

        )



    def save_product(
            self,
            sku,
            data
    ):


        self.save_json(

            self.product_file(sku),

            data

        )