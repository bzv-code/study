import logging
import sys

from pathlib import Path



def get_logger(
        name: str,
        log_file: Path | None = None
):


    logger = logging.getLogger(
        name
    )


    logger.setLevel(
        logging.INFO
    )


    logger.propagate = False



    # защита от повторного добавления handlers

    if logger.handlers:

        return logger



    formatter = logging.Formatter(

        "%(asctime)s | "
        "%(levelname)s | "
        "%(name)s | "
        "%(message)s",

        datefmt="%Y-%m-%d %H:%M:%S"

    )



    # Console handler

    console = logging.StreamHandler(
        sys.stdout
    )


    console.setFormatter(
        formatter
    )


    logger.addHandler(
        console
    )



    # File handler

    if log_file:


        file_handler = logging.FileHandler(

            log_file,

            encoding="utf-8"

        )


        file_handler.setFormatter(
            formatter
        )


        logger.addHandler(
            file_handler
        )



    return logger