import json
from pathlib import Path


JSON_FILE = Path(
    r"C:\Backup\Облако\PycharmProjects\wb_parser_project\wb_parser\data\sessions\2026-07-15_10-23-59\search_debug\search_catalog_1784100241.json"
)


def extract_ids(file_path):

    print("Чтение JSON...")

    with open(
            file_path,
            "r",
            encoding="utf-8"
    ) as f:

        data = json.load(f)


    products = data.get(
        "products",
        []
    )


    print(
        f"Найдено товаров: {len(products)}"
    )


    ids = []


    for product in products:

        product_id = product.get(
            "id"
        )

        if product_id:

            ids.append(
                product_id
            )


    return ids



def save_ids(ids):

    output = (
        JSON_FILE.parent
        /
        "product_ids.txt"
    )


    with open(
            output,
            "w",
            encoding="utf-8"
    ) as f:


        for item in ids:

            f.write(
                f"{item}\n"
            )


    print(
        f"ID сохранены: {output}"
    )



def main():

    ids = extract_ids(
        JSON_FILE
    )


    save_ids(
        ids
    )


    print(
        "\nПервые 10 ID:"
    )


    for item in ids[:10]:

        print(
            item
        )



if __name__ == "__main__":

    main()