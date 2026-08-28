from __future__ import annotations


from datetime import date


from client.moex_client import MoexClient


from models.dividend_model import DividendModel


from utils.logger import get_logger



logger = get_logger(__name__)







class DividendService:
    """
    Сервис работы с дивидендами акций MOEX.


    Отвечает только за бизнес-логику.


    Источник данных:

        MoexClient


    API:

        /iss/securities/{SECID}/dividends.json

    """





    def __init__(
        self,
        client: MoexClient,
    ) -> None:


        self.client = client



        logger.debug(
            "DividendService initialized"
        )









    def get(
        self,
        secid: str,
    ) -> list[DividendModel]:
        """
        Получить историю дивидендов акции.


        Пример:

            TATN


        Возвращает:

            list[DividendModel]

        """



        logger.debug(

            "GET DIVIDENDS SECID=%s",

            secid,

        )





        if not secid:



            logger.warning(

                "GET DIVIDENDS WITHOUT SECID"

            )



            raise ValueError(

                "SECID не указан"

            )







        secid = secid.upper()






        try:



            response = self.client.get(

                f"/securities/{secid}/dividends.json"

            )



        except Exception as error:



            logger.exception(

                "MOEX DIVIDENDS REQUEST ERROR SECID=%s ERROR=%s",

                secid,

                error,

            )


            raise







        dividends_block = response.get(

            "dividends",

            {}

        )



        if not dividends_block:



            logger.info(

                "EMPTY DIVIDENDS BLOCK SECID=%s",

                secid,

            )


            return []







        columns = dividends_block.get(

            "columns",

            []

        )



        rows = dividends_block.get(

            "data",

            []

        )







        if not columns or not rows:



            logger.info(

                "NO DIVIDENDS FOUND SECID=%s",

                secid,

            )


            return []









        result: list[DividendModel] = []







        for row in rows:



            if len(row) != len(columns):



                logger.warning(

                    "INVALID DIVIDEND ROW SECID=%s ROW=%s",

                    secid,

                    row,

                )


                continue





            item = dict(

                zip(

                    columns,

                    row,

                )

            )







            try:



                dividend = DividendModel(



                    secid=item.get(

                        "secid",

                        "",

                    ),



                    isin=item.get(

                        "isin",

                        "",

                    ),




                    registry_close_date=self._parse_date(

                        item.get(

                            "registryclosedate"

                        )

                    ),




                    value=float(

                        item.get(

                            "value"

                        )

                        or 0

                    ),




                    currency=item.get(

                        "currencyid",

                        "",

                    ),



                )



            except Exception as error:



                logger.exception(

                    "DIVIDEND MODEL ERROR SECID=%s DATA=%s ERROR=%s",

                    secid,

                    item,

                    error,

                )


                continue







            result.append(

                dividend

            )









        logger.info(

            "DIVIDENDS FOUND SECID=%s COUNT=%s",

            secid,

            len(result),

        )



        return result










    def get_last(
        self,
        secid: str,
    ) -> DividendModel | None:
        """
        Получить последний дивиденд.


        Используется:

        - уведомления
        - аналитика

        """



        dividends = self.get(

            secid

        )



        if not dividends:


            return None







        return max(

            dividends,

            key=lambda x: x.registry_close_date or date.min,

        )











    @staticmethod
    def _parse_date(
        value: str | None,
    ) -> date | None:
        """
        Преобразование даты MOEX:


            2025-06-02


        в:


            date(2025,6,2)

        """



        if not value:



            return None







        try:



            return date.fromisoformat(

                value

            )



        except ValueError:



            logger.warning(

                "INVALID DIVIDEND DATE VALUE=%s",

                value,

            )



            return None