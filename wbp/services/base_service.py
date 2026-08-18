from browser.wb_browser import WBBrowser
from storage.session_manager import SessionManager


class BaseService:


    def __init__(
            self,
            logger
    ):

        self.logger = logger


        self.session = SessionManager(
            logger
        )


        self.logger.info(
            "Создана новая сессия: %s",
            self.session.session_dir
        )


        self.browser = None



    def start(self):

        self.logger.info(
            "Запуск браузера"
        )


        try:

            self.browser = WBBrowser(

                session=self.session,

                logger=self.logger

            )


            self.browser.start()


            self.logger.info(
                "Браузер успешно запущен"
            )


        except Exception as e:

            self.logger.exception(
                "Ошибка запуска браузера: %s",
                e
            )

            raise



    def stop(self):

        self.logger.info(
            "Остановка браузера"
        )


        try:

            if self.browser:

                self.browser.close()


        except Exception as e:

            self.logger.exception(
                "Ошибка закрытия браузера: %s",
                e
            )