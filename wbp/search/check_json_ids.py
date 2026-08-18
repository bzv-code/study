import json
from pathlib import Path


FILE = Path(
    r"C:\Backup\Облако\PycharmProjects\wb_parser_project\wb_parser\data\sessions\2026-07-14_12-04-06\search_debug\json\__internal_banners_shelfs_search_query_кроссовки_мужские_2.json"
)


def find_ids(obj, result=None):
    """
    Рекурсивный поиск id в любом JSON
    """

    if result is None:
        result = set()


    if isinstance(obj, dict):

        for key, value in obj.items():

            key_lower = key.lower()

            if key_lower in [
                "id",
                "nmid",
                "nm_id",
                "productid",
                "product_id"
            ]:

                if isinstance(value, (int, str)):

                    result.add(str(value))


            find_ids(
                value,
                result
            )


    elif isinstance(obj, list):

        for item in obj:

            find_ids(
                item,
                result
            )


    return result



def main():

    print("Чтение файла:")
    print(FILE)


    if not FILE.exists():

        print("Файл не найден")
        return



    try:

        text = FILE.read_text(
            encoding="utf-8"
        )


        # проверяем начало файла

        print("\nПервые 200 символов:")
        print(text[:200])


        data = json.loads(text)


    except Exception as e:

        print("\nОшибка чтения JSON:")
        print(e)
        return



    ids = find_ids(
        data
    )


    print("\n======================")
    print(
        f"Найдено уникальных ID: {len(ids)}"
    )
    print("======================")


    for item in list(ids)[:20]:

        print(item)



if __name__ == "__main__":

    main()