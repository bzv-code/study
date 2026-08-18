from logger.logger import get_logger
from api.wb_client import WBClient



def main():


    logger = get_logger(
        "WB_API_TEST"
    )


    client = WBClient(
        logger
    )


    data = client.get_product(
        1046254595
    )


    print(
        data.keys()
    )



if __name__ == "__main__":

    main()