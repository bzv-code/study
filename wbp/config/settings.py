from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


RAW_JSON_DIR = (
    BASE_DIR /
    "data" /
    "raw"
)


RESULT_FILE = (
    BASE_DIR /
    "data" /
    "products.xlsx"
)

BROWSER_SESSION_DIR = (

    BASE_DIR
    /
    "data"
    /
    "browser_session"

)



MODE = "auto"


# Через сколько часов обновлять cookies
SESSION_REFRESH_HOURS = 24


# количество потоков для будущего async режима
MAX_WORKERS = 20



# список товаров для теста

PRODUCTS = [

    1046254595,

    1009481833,

]