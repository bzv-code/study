import time


class RateLimiter:
    """
    Ограничение количества запросов.

    max_requests:
        количество запросов

    period:
        период в секундах
    """


    def __init__(
        self,
        max_requests: int = 3,
        period: float = 1.0,
    ):

        self.delay = period / max_requests



    def wait(self):

        time.sleep(
            self.delay
        )