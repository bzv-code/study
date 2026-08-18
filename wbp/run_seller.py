from logger.logger import get_logger


from seller.seller_debug import SellerDebug
from browser.wb_browser import WBBrowser


from services.seller_product_service import (
    SellerProductService
)


from parser.sku_loader import (
    SkuLoader
)


from storage.session_manager import SessionManager



SELLER_URL = (
    "https://www.wildberries.ru/seller/4032338"
)



def main():


    logger = get_logger(
        "WB_SELLER_FULL"
    )


    # =========================
    # SESSION
    # =========================


    session = SessionManager(
        logger
    )


    logger.info(
        "Session: %s",
        session.session_dir
    )



    # =========================
    # BROWSER
    # =========================


    browser = WBBrowser(
        session,
        logger
    )


    debug = SellerDebug(

        browser,

        logger,

        session.session_dir

    )



    try:


        browser.start()


        debug.attach()



        logger.info(
            "Открываем магазин %s",
            SELLER_URL
        )



        browser.page.goto(

            SELLER_URL,

            wait_until="domcontentloaded",

            timeout=60000

        )



        browser.page.wait_for_timeout(
            15000
        )



        browser.page.reload(

            wait_until="domcontentloaded",

            timeout=60000

        )



        browser.page.wait_for_timeout(
            10000
        )



        browser.page.mouse.wheel(
            0,
            5000
        )


        browser.page.wait_for_timeout(
            10000
        )



        logger.info(
            "Каталог получен"
        )



        browser.save_session()



    except Exception as e:


        logger.exception(
            "Ошибка браузера: %s",
            e
        )


    finally:


        browser.close()



    # =========================
    # SKU
    # =========================


    loader = SkuLoader(

        session.session_dir,

        logger

    )


    skus = loader.load()



    logger.info(
        "SKU найдено: %s",
        len(skus)
    )



    if not skus:

        return



    # =========================
    # PRODUCTS
    # =========================


    service = SellerProductService(

        logger,

        session

    )


    service.run(
        skus
    )



    logger.info(
        "ГОТОВО"
    )




if __name__ == "__main__":

    main()