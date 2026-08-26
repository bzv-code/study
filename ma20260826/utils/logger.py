from __future__ import annotations

import logging
import os
from pathlib import Path
from datetime import datetime

from dotenv import load_dotenv


load_dotenv()



# ------------------------------------------------------
# Настройки
# ------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent


LOG_DIR = Path(
    os.getenv(
        "LOG_DIR",
        "logs",
    )
)


if not LOG_DIR.is_absolute():

    LOG_DIR = BASE_DIR / LOG_DIR



LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "DEBUG",
).upper()



LOG_FILE_ENABLED = os.getenv(
    "LOG_FILE",
    "true",
).lower() == "true"




# ------------------------------------------------------
# Создание папки логов
# ------------------------------------------------------

LOG_DIR.mkdir(
    parents=True,
    exist_ok=True,
)



LOG_FILE = (

    LOG_DIR /

    f"moex_api_{datetime.now().strftime('%Y_%m_%d')}.log"

)




# ------------------------------------------------------
# Logger factory
# ------------------------------------------------------

def get_logger(
    name: str,
) -> logging.Logger:
    """
    Получение логгера приложения.


    Пример:

        logger = get_logger(__name__)


    Уровни:

        DEBUG
        INFO
        WARNING
        ERROR

    """


    logger = logging.getLogger(
        name
    )



    if logger.handlers:

        return logger



    level = getattr(

        logging,

        LOG_LEVEL,

        logging.DEBUG,

    )


    logger.setLevel(
        level
    )



    formatter = logging.Formatter(

        fmt=(

            "%(asctime)s | "

            "%(levelname)s | "

            "%(name)s | "

            "%(message)s"

        ),

        datefmt="%Y-%m-%d %H:%M:%S",

    )



    # --------------------------------------------------
    # Console
    # --------------------------------------------------

    console_handler = logging.StreamHandler()


    console_handler.setLevel(
        level
    )


    console_handler.setFormatter(
        formatter
    )


    logger.addHandler(
        console_handler
    )



    # --------------------------------------------------
    # File
    # --------------------------------------------------

    if LOG_FILE_ENABLED:


        file_handler = logging.FileHandler(

            LOG_FILE,

            encoding="utf-8",

        )


        file_handler.setLevel(
            level
        )


        file_handler.setFormatter(
            formatter
        )


        logger.addHandler(
            file_handler
        )



    logger.propagate = False


    return logger