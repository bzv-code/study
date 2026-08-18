from typing import Any


def print_json_tree(
        data: Any,
        name: str = "root",
        level: int = 0,
        max_list_items: int = 3
):
    """
    Рекурсивный вывод структуры JSON.

    Показывает:
    - название поля
    - тип данных
    - пример значения
    - вложенность
    """

    indent = "    " * level


    if isinstance(data, dict):

        print(
            f"{indent}{name} : dict"
        )

        for key, value in data.items():

            print_json_tree(
                value,
                name=key,
                level=level + 1,
                max_list_items=max_list_items
            )


    elif isinstance(data, list):

        print(
            f"{indent}{name} : list[{len(data)}]"
        )


        for index, item in enumerate(data[:max_list_items]):

            print_json_tree(
                item,
                name=f"[{index}]",
                level=level + 1,
                max_list_items=max_list_items
            )


    else:

        value_preview = str(data)

        if len(value_preview) > 80:
            value_preview = value_preview[:80] + "..."


        print(
            f"{indent}{name} : "
            f"{type(data).__name__} "
            f"= {value_preview}"
        )