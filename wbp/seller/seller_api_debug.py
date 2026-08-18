import json
import httpx
from pathlib import Path


URL = """
https://www.wildberries.ru/__internal/u-catalog/sellers/v4/catalog
"""


PARAMS = {
    "ab_testid": "new_cb_1",
    "appType": 1,
    "curr": "rub",
    "dest": -1257786,
    "hide_dtype": 15,
    "hide_vflags": 4294967296,
    "lang": "ru",
    "page": 1,
    "sort": "popular",
    "spp": 30,
    "supplier": 4032338,
}


def main():

    headers = {
        "User-Agent":
        "Mozilla/5.0"
    }


    with httpx.Client(
        headers=headers,
        timeout=30
    ) as client:

        r = client.get(
            URL,
            params=PARAMS
        )


        print(
            r.status_code
        )


        print(
            r.text[:1000]
        )


        Path(
            "catalog_test.json"
        ).write_text(
            r.text,
            encoding="utf-8"
        )


if __name__ == "__main__":
    main()