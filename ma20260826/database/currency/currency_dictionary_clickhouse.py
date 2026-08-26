from __future__ import annotations


from typing import Final



CURRENCY_NAMES: Final[dict[str, str]] = {


    "CNYRUB_TOM": "Китайский юань",


    "TRYRUB_TOM": "Турецкая лира",


    "KZTRUB_TOM": "Казахстанский тенге",


    "BYNRUB_TOM": "Белорусский рубль",


    "AMDRUB_TOM": "Армянский драм",


}





def get_currency_name(
    ticker: str,
) -> str:
    """
    Получить название валюты по тикеру MOEX.

    Пример:

        CNYRUB_TOM
        ->
        Китайский юань


    Если тикер отсутствует
    возвращает сам тикер.
    """


    return CURRENCY_NAMES.get(

        ticker,

        ticker,

    )