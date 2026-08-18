import json
from pathlib import Path


JSON_FILE = Path(
    r"C:\Backup\Облако\PycharmProjects\wb_parser_project\wb_parser\data\seller_debug\seller_catalog_1783953110.json"
)


PRODUCT_IDS = [
    "767122067",
    "827248349",
    "840418103",
    "820238061",
    "760580782",
    "693025069",
    "1029769341",
    "692998923",
    "701764621",
    "896712708",
    "693025070",
    "701764620",
]


# Здесь будут храниться все найденные пути
FOUND = {
    sku: []
    for sku in PRODUCT_IDS
}


def search_ids(obj, path="root"):

    if isinstance(obj,dict):

        for key, value in obj.items():

            value_str = str(value)

            if value_str in FOUND:

                FOUND[value_str].append(
                    {
                        "path": path,
                        "key": key,
                        "value": value
                    }
                )

            search_ids(
                value,
                f"{path}.{key}"
            )


    elif isinstance(obj,list):

        for index,item in enumerate(obj):

            search_ids(
                item,
                f"{path}[{index}]"
            )


def main():

    print("=" * 80)
    print("Файл:")
    print(JSON_FILE)
    print("=" * 80)

    with open(
        JSON_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)

    search_ids(data)

    print()
    print("=" * 80)
    print("РЕЗУЛЬТАТ")
    print("=" * 80)

    found_count = 0

    for sku in PRODUCT_IDS:

        if FOUND[sku]:

            found_count += 1

            print(f"\n✅ SKU {sku} НАЙДЕН ({len(FOUND[sku])} совпадений)")

            for item in FOUND[sku]:

                print(f"   PATH : {item['path']}")
                print(f"   KEY  : {item['key']}")

        else:

            print(f"\n❌ SKU {sku} НЕ НАЙДЕН")

    print()
    print("=" * 80)
    print(f"Найдено {found_count} из {len(PRODUCT_IDS)} SKU")
    print("=" * 80)


if __name__ == "__main__":
    main()