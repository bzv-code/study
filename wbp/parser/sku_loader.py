import json

from pathlib import Path



class SkuLoader:


    def __init__(
            self,
            path,
            logger=None
    ):

        self.path = Path(path)
        self.logger = logger



    def load(self):


        if not self.path.exists():

            raise FileNotFoundError(
                f"Папка сессии не найдена: {self.path}"
            )



        files = list(

            self.path.glob(
                "seller_sku_*.json"
            )

        )



        if not files:


            raise FileNotFoundError(

                f"Файлы seller_sku_*.json не найдены: {self.path}"

            )



        latest_file = max(

            files,

            key=lambda x: x.stat().st_mtime

        )



        if self.logger:


            self.logger.info(

                "Выбран файл SKU: %s",

                latest_file

            )



        try:


            with open(

                    latest_file,

                    "r",

                    encoding="utf-8"

            ) as f:


                data = json.load(f)



        except json.JSONDecodeError as e:


            raise ValueError(

                f"Ошибка чтения JSON SKU файла {latest_file}: {e}"

            )




        if not isinstance(

                data,

                list

        ):


            raise ValueError(

                "seller_sku JSON должен содержать список товаров"

            )




        sku_list = []

        sku_set = set()



        for item in data:



            if not isinstance(

                    item,

                    dict

            ):

                continue



            sku = item.get(
                "id"
            )



            if sku is None:


                continue



            try:


                sku = int(sku)


            except (TypeError, ValueError):


                if self.logger:


                    self.logger.warning(

                        "Некорректный SKU пропущен: %s",

                        sku

                    )


                continue




            if sku not in sku_set:


                sku_set.add(
                    sku
                )


                sku_list.append(
                    sku
                )




        if self.logger:


            self.logger.info(

                "Загружено уникальных SKU: %s",

                len(sku_list)

            )



        return sku_list