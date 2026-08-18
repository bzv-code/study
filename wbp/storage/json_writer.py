import json


class JsonWriter:


    def __init__(
            self,
            session,
            logger
    ):

        self.session = session
        self.logger = logger



    def save(
            self,
            sku,
            data
    ):

        file = self.session.response_file(
            sku
        )


        try:

            with open(
                    file,
                    "w",
                    encoding="utf-8"
            ) as f:


                json.dump(
                    data,
                    f,
                    ensure_ascii=False,
                    indent=4
                )



            self.logger.info(
                "RAW JSON сохранен: %s",
                file
            )



        except Exception as e:


            self.logger.exception(
                "Ошибка сохранения JSON: %s",
                e
            )

            raise