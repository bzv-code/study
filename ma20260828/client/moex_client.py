from __future__ import annotations

from typing import Any

import time
import httpx


from utils.logger import get_logger



logger = get_logger(__name__)




class MoexClient:
    """
    Клиент MOEX ISS API.

    Возможности:

    - ограничение запросов;
    - максимум 3 запроса/сек;
    - повтор запросов при временных ошибках;
    - работа через context manager.
    """


    BASE_URL = "https://iss.moex.com/iss"


    RETRY_STATUS_CODES = {

        429,

        500,

        502,

        503,

        504,

    }



    def __init__(
        self,
        timeout: int = 30,
        max_requests_per_second: int = 3,
        retry_count: int = 3,
        retry_delay: int = 2,
    ) -> None:


        self.client = httpx.Client(

            timeout=httpx.Timeout(

                connect=10,

                read=timeout,

                write=timeout,

                pool=timeout,

            ),

            headers={

                "User-Agent":
                    "Mozilla/5.0 (Windows NT 10.0) MOEX Client",

                "Accept":
                    "application/json",

            },

        )


        self.request_delay = (

            1.0 /

            max_requests_per_second

        )


        self.last_request_time = 0.0


        self.retry_count = retry_count

        self.retry_delay = retry_delay



        logger.debug(

            "MOEX CLIENT INITIALIZED timeout=%s retry_count=%s",

            timeout,

            retry_count,

        )





    def _wait_rate_limit(
        self,
    ) -> None:
        """
        Ограничитель количества запросов.
        """


        now = time.time()


        elapsed = (

            now -

            self.last_request_time

        )



        if elapsed < self.request_delay:


            sleep_time = (

                self.request_delay -

                elapsed

            )


            logger.debug(

                "RATE LIMIT WAIT %.2f sec",

                sleep_time,

            )


            time.sleep(

                sleep_time

            )



        self.last_request_time = time.time()





    def get(
        self,
        path: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        GET запрос ISS API.

        Есть автоматический retry.
        """


        url = (

            f"{self.BASE_URL}/{path}"

        )


        attempt = 1



        while attempt <= self.retry_count + 1:



            self._wait_rate_limit()



            logger.debug(

                "REQUEST ATTEMPT=%s",

                attempt,

            )


            logger.debug(

                "REQUEST URL=%s",

                url,

            )



            if params:


                logger.debug(

                    "REQUEST PARAMS=%s",

                    params,

                )



            try:


                start_time = time.time()


                response = self.client.get(

                    url,

                    params=params,

                )


                elapsed = (

                    time.time()

                    -

                    start_time

                )



                logger.debug(

                    "RESPONSE STATUS=%s TIME=%.3f sec",

                    response.status_code,

                    elapsed,

                )



                if response.status_code in self.RETRY_STATUS_CODES:



                    if attempt <= self.retry_count:


                        logger.warning(

                            "RETRY STATUS=%s AFTER %s SEC",

                            response.status_code,

                            self.retry_delay,

                        )


                        time.sleep(

                            self.retry_delay

                        )


                        attempt += 1

                        continue



                response.raise_for_status()



                logger.debug(

                    "JSON RESPONSE RECEIVED"

                )



                return response.json()



            except httpx.RequestError as error:



                logger.error(

                    "NETWORK ERROR: %s",

                    error,

                )



                if attempt <= self.retry_count:


                    logger.warning(

                        "RETRY AFTER %s SEC",

                        self.retry_delay,

                    )


                    time.sleep(

                        self.retry_delay

                    )


                    attempt += 1

                    continue



                raise



        raise RuntimeError(

            "MOEX request failed after retries"

        )





    # ------------------------------------------------------
    # Engines
    # ------------------------------------------------------


    def get_engines(
        self,
    ) -> dict[str, Any]:


        return self.get(

            "engines.json"

        )





    def get_markets(
        self,
        engine: str,
    ) -> dict[str, Any]:


        return self.get(

            f"engines/{engine}/markets.json"

        )





    # ------------------------------------------------------
    # Securities
    # ------------------------------------------------------


    def get_market_securities(
        self,
        engine: str,
        market: str,
        start: int = 0,
        limit: int = 100,
    ) -> dict[str, Any]:


        return self.get(


            f"engines/{engine}/markets/{market}/securities.json",


            params={

                "start": start,

                "limit": limit,

            },


        )





    def get_security(
        self,
        secid: str,
    ) -> dict[str, Any]:


        return self.get(

            f"securities/{secid}.json"

        )





    # ------------------------------------------------------
    # Candles
    # ------------------------------------------------------


    def get_candles(
        self,
        engine: str,
        market: str,
        security: str,
        date_from: str,
        date_till: str,
        interval: int = 24,
        start: int = 0,
    ) -> dict[str, Any]:


        return self.get(


            (

                f"engines/{engine}/markets/{market}/"

                f"securities/{security}/candles.json"

            ),


            params={


                "from": date_from,

                "till": date_till,

                "interval": interval,

                "start": start,


            },


        )





    # ------------------------------------------------------
    # Context manager
    # ------------------------------------------------------


    def close(
        self,
    ) -> None:


        self.client.close()


        logger.debug(

            "MOEX CLIENT CLOSED"

        )




    def __enter__(
        self,
    ) -> "MoexClient":


        return self




    def __exit__(
        self,
        exc_type,
        exc_val,
        exc_tb,
    ) -> None:


        self.close()