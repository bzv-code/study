import json
import time

from pathlib import Path


from logger.logger import get_logger

from storage.project_session import ProjectSession

from browser.wb_browser import WBBrowser

from search.search_debug import SearchDebug

from services.search_product_service import SearchProductService



SEARCH_URL = (
    "https://www.wildberries.ru/catalog/0/search.aspx?"
    "search=кроссовки+мужские"
)



def wait_for_search_json(
        folder,
        logger,
        timeout=60
):


    logger.info(
        "Ожидание JSON поисковой выдачи"
    )


    start = time.time()



    while True:



        files = list(
            Path(folder)
            .glob(
                "search_catalog_*.json"
            )
        )



        if files:


            file = max(
                files,
                key=lambda x: x.stat().st_mtime
            )


            logger.info(
                "Найден файл поиска: %s",
                file
            )


            return file




        if time.time() - start > timeout:


            raise TimeoutError(
                "JSON поисковой выдачи не найден"
            )



        time.sleep(
            1
        )





def extract_ids(
        file,
        logger
):


    logger.info(
        "Чтение JSON поиска: %s",
        file
    )



    with open(
            file,
            "r",
            encoding="utf-8"
    ) as f:


        data = json.load(
            f
        )



    products = data.get(
        "products",
        []
    )



    if not products:


        raise Exception(
            "В JSON нет products"
        )



    ids = []



    for product in products:


        sku = product.get(
            "id"
        )


        if sku:

            ids.append(
                sku
            )



    logger.info(
        "Найдено товаров: %s",
        len(ids)
    )


    return ids





def wait_and_scroll(
        page,
        logger
):


    logger.info(
        "Ожидание загрузки WB"
    )


    page.wait_for_timeout(
        15000
    )



    logger.info(
        "Первый скролл"
    )


    page.mouse.wheel(
        0,
        800
    )


    page.wait_for_timeout(
        5000
    )



    logger.info(
        "Второй скролл"
    )


    page.mouse.wheel(
        0,
        1500
    )


    page.wait_for_timeout(
        5000
    )





def main():


    logger = get_logger(
        "WB_SEARCH"
    )



    project = ProjectSession()



    logger.info(
        "Сессия: %s",
        project.path
    )



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



        #
        # подключаем ДО открытия страницы
        #

        debug.attach()



        logger.info(
            "Открываем поиск WB"
        )



        browser.page.goto(

            SEARCH_URL,

            wait_until="domcontentloaded",

            timeout=60000

        )



        logger.info(
            "Страница открыта"
        )



        wait_and_scroll(

            browser.page,

            logger

        )



        logger.info(
            "Ждем файл выдачи"
        )



        json_file = wait_for_search_json(

            project.path
            /
            "search_debug",

            logger

        )



        ids = extract_ids(

            json_file,

            logger

        )



        #
        # ограничиваем TOP 100
        #

        ids = ids[:100]



        logger.info(
            "Передаем %s товаров в парсер",
            len(ids)
        )



        service = SearchProductService(
            logger
        )



        service.run(
            ids
        )



        logger.info(
            "Готово. Результат сохранен"
        )



        while True:


            browser.page.wait_for_timeout(
                1000
            )




    except KeyboardInterrupt:


        logger.info(
            "Остановка пользователем"
        )



    except Exception as e:


        logger.exception(
            "Ошибка run_search: %s",
            e
        )



    finally:


        logger.info(
            "Завершение"
        )





if __name__ == "__main__":

    main()