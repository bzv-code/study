from seller.seller_catalog_api import SellerCatalogAPI

from parser.sku_loader import SkuLoader

from services.seller_product_service import SellerProductService



class SellerService:


    def __init__(
            self,
            logger
    ):

        self.logger = logger



    def run(
            self,
            seller_id
    ):



        # =================================
        # 1. Получаем каталог
        # =================================


        api = SellerCatalogAPI(
            self.logger
        )


        catalog = api.get_catalog(
            seller_id
        )



        products = catalog.get(
            "products",
            []
        )


        self.logger.info(
            "Получено товаров из каталога: %s",
            len(products)
        )



        # =================================
        # 2. Создаем временный SKU файл
        # =================================


        sku_file = SellerCatalogAPI.save_sku(
            products
        )



        # =================================
        # 3. Парсим карточки
        # =================================


        loader = SkuLoader(
            "data/seller_debug",
            self.logger
        )


        skus = loader.load()



        service = SellerProductService(
            self.logger
        )


        service.run(
            skus
        )