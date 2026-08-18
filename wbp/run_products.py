from logger.logger import get_logger

from config.settings import (
    PRODUCTS,
    BROWSER_SESSION_DIR,
    SESSION_REFRESH_HOURS
)


from services.browser_session_checker import (
    BrowserSessionChecker
)


from browser.browser_session import BrowserSession


from services.api_product_service import (
    APIProductService
)




def refresh_browser_session(logger):


    logger.info(
        "Обновление Browser Session"
    )


    session = BrowserSession(
        logger
    )


    try:

        session.start()


        session.open_product(
            PRODUCTS[0]
        )


        session.save()



    finally:

        session.close()





def main():


    logger = get_logger(
        "WB_PRODUCTION"
    )



    checker = BrowserSessionChecker(

        BROWSER_SESSION_DIR,

        SESSION_REFRESH_HOURS

    )



    if checker.is_valid():


        logger.info(
            "Browser Session актуальна"
        )


    else:


        logger.info(
            "Browser Session устарела"
        )


        refresh_browser_session(
            logger
        )



    logger.info(
        "Запуск API режима"
    )


    service = APIProductService(
        logger
    )


    service.run(
        PRODUCTS
    )




if __name__ == "__main__":

    main()