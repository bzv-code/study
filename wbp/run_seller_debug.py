from logger.logger import get_logger

from browser.wb_browser import WBBrowser
from seller.seller_debug import SellerDebug


SELLER_URL = (
    "https://www.wildberries.ru/seller/4032338"
)


def main():

    logger = get_logger(
        "WB_SELLER_DEBUG"
    )


    browser = WBBrowser(
        None,
        logger
    )


    debug = SellerDebug(
        browser,
        logger
    )


    try:

        logger.info(
            "Запуск браузера"
        )

        browser.start()


        logger.info(
            "Подключаем перехват запросов"
        )

        debug.attach()


        logger.info(
            "Открываем магазин: %s",
            SELLER_URL
        )


        browser.page.goto(
            SELLER_URL,
            wait_until="domcontentloaded",
            timeout=60000
        )


        logger.info(
            "Первая загрузка завершена"
        )


        browser.page.wait_for_timeout(
            10000
        )


        logger.info(
            "Перезагрузка страницы"
        )


        browser.page.reload(
            wait_until="domcontentloaded",
            timeout=60000
        )


        logger.info(
            "Reload завершен"
        )


        browser.page.wait_for_timeout(
            20000
        )


        logger.info(
            "Прокрутка страницы"
        )


        browser.page.mouse.wheel(
            0,
            5000
        )


        browser.page.wait_for_timeout(
            15000
        )


        logger.info(
            "Сбор завершен"
        )


    except Exception as e:

        logger.exception(
            "Ошибка выполнения: %s",
            e
        )


    finally:

        logger.info(
            "Закрытие браузера"
        )

        browser.close()


        logger.info(
            "Браузер закрыт"
        )



if __name__ == "__main__":

    main()