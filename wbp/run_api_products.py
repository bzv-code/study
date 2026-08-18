from services.api_product_service import APIProductService
from logger.logger import get_logger



URLS = [

"https://www.wildberries.ru/catalog/1046254595/detail.aspx",

"https://www.wildberries.ru/catalog/1009481833/detail.aspx",

]



def main():


    logger = get_logger(
        "WB_API"
    )


    service = APIProductService(
        logger
    )


    service.run(
        URLS
    )



if __name__=="__main__":

    main()