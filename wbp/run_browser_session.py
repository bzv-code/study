from browser.browser_session import BrowserSession
from logger.logger import get_logger



SKU = "1046254595"



def main():


    logger = get_logger(
        "WB_BROWSER_SESSION"
    )


    session = BrowserSession(
        logger
    )


    try:


        session.start()


        session.open_product(
            SKU
        )


        session.save()



    finally:


        session.close()



if __name__ == "__main__":

    main()