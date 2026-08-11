import asyncio


from app.services.alert_monitor_service import (
    AlertMonitorService
)



print(
    "ALERT PRICE MONITOR LIFECYCLE SERVICE LOADED"
)



class AlertMonitorLifecycleService:
    """
    Управление жизненным циклом
    фонового мониторинга уведомлений.

    Задачи:
    - запускать монитор один раз
    - не создавать дубликаты при reconnect MAX API
    - корректно останавливать задачу
    """



    _task: asyncio.Task | None = None



    def __init__(self):

        self.monitor_service = AlertMonitorService()



    # ==================================================
    # START
    # ==================================================

    async def start(self):
        """
        Запуск фонового мониторинга
        """

        task = self.__class__._task


        # ==============================================
        # Проверка существующего запуска
        # ==============================================

        if task and not task.done():

            print(
                "ALERT MONITOR ALREADY RUNNING"
            )

            return



        print(
            "START ALERT PRICE MONITOR"
        )



        self.__class__._task = asyncio.create_task(

            self.monitor_service.run()

        )


        print(
            "ALERT MONITOR TASK CREATED"
        )



    # ==================================================
    # STOP
    # ==================================================

    async def stop(self):
        """
        Остановка фонового мониторинга
        """



        task = self.__class__._task



        if not task:

            print(
                "ALERT MONITOR NOT RUNNING"
            )

            return



        print(
            "STOP ALERT PRICE MONITOR"
        )



        task.cancel()



        try:

            await task


        except asyncio.CancelledError:

            print(
                "ALERT MONITOR CANCELLED"
            )



        finally:

            self.__class__._task = None



            print(
                "ALERT MONITOR TASK CLEARED"
            )



    # ==================================================
    # STATUS
    # ==================================================

    @classmethod
    def is_running(cls) -> bool:

        task = cls._task


        return (

            task is not None

            and not task.done()

        )