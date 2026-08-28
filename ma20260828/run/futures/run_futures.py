from __future__ import annotations


from client.moex_client import MoexClient


from catalog.futures_catalog import (
    FuturesCatalog,
)


from services.futures_service import (
    FuturesService,
)


from database.client_clickhouse import (
    ClickHouseClient,
)


from database.futures.futures_clickhouse import (
    FuturesClickHouse,
)


from database.futures.writer_futures_clickhouse import (
    FuturesWriterClickHouse,
)


from utils.logger import get_logger



logger = get_logger(__name__)







TABLE_NAME = "moex_api.moex_futures"









def main() -> None:
    """
    Загрузка каталога фьючерсов MOEX
    в ClickHouse.


    Источник:

        MOEX ISS

        /iss/engines/futures/markets/forts/securities.json


    Назначение:

        moex_api.moex_futures

    """



    print("=" * 80)

    print(
        "RUN FUTURES LOAD"
    )

    print("=" * 80)







    futures = []






    # ==================================================
    # MOEX
    # ==================================================


    with MoexClient() as client:



        logger.info(

            "MOEX CLIENT CREATED"

        )





        catalog = FuturesCatalog(

            client

        )





        service = FuturesService(

            catalog

        )







        logger.info(

            "LOAD FUTURES CATALOG"

        )





        catalog.load_futures()






        futures = service.search(

            ""

        )





        if not futures:



            futures = catalog.get_all_items()







        logger.info(

            "FUTURES RECEIVED COUNT=%s",

            len(futures),

        )






        print()

        print(

            "TOTAL FUTURES:",

            len(futures),

        )









    # ==================================================
    # CLICKHOUSE
    # ==================================================


    if not futures:


        logger.warning(

            "NO FUTURES DATA RECEIVED"

        )


        print(

            "NO FUTURES DATA"

        )


        return








    logger.info(

        "START CLICKHOUSE INSERT"

    )







    with ClickHouseClient() as client:



        futures_clickhouse = FuturesClickHouse(



            client,


            table_name=TABLE_NAME,



        )






        writer = FuturesWriterClickHouse(



            futures_clickhouse



        )








        writer.write(

            futures

        )







    logger.info(

        "CLICKHOUSE INSERT FINISHED"

    )







    print()

    print("=" * 80)

    print(
        "RUN COMPLETE FUTURES"
    )

    print("=" * 80)








if __name__ == "__main__":

    main()