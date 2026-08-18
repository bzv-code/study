from logger.logger import get_logger

from storage.project_session import ProjectSession

from browser.wb_browser import WBBrowser

from search.search_debug import SearchDebug



URL = (
    "https://www.wildberries.ru/catalog/0/search.aspx?"
    "search=кроссовки+мужские"
)



def main():


    logger = get_logger(
        "WB_CAPTURE"
    )


    project = ProjectSession()


    browser = WBBrowser(
        None,
        logger
    )


    try:


        browser.start()


        debug = SearchDebug(
            browser,
            logger,
            project.path
        )


        debug.attach()



        logger.info(
            "Открываем поиск WB"
        )


        browser.page.goto(

            URL,

            wait_until="domcontentloaded",

            timeout=60000

        )


        logger.info(
            "Ждем загрузку"
        )


        browser.page.wait_for_timeout(
            30000
        )



        logger.info(
            "Делаем скрол"
        )


        browser.page.mouse.wheel(
            0,
            1000
        )


        browser.page.wait_for_timeout(
            10000
        )



        logger.info(
            "Оставляем браузер"
        )


        while True:

            browser.page.wait_for_timeout(
                1000
            )



    except Exception as e:

        logger.exception(e)



if __name__ == "__main__":

    main()