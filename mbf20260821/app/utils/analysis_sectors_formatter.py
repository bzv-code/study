print(
    "ANALYSIS SECTORS FORMATTER LOADED"
)


class AnalysisSectorsFormatter:


    @classmethod
    def format(

            cls,

            analysis: dict

    ) -> str:


        if not analysis:

            return (
                "❌ Нет данных по секторам"
            )


        period = analysis.get(

            "period",

            7

        )


        text = (

            "🌎 Анализ секторов\n\n"

            f"📈 ТОП 5 роста за {period} дней:\n\n"

        )



        # ==================================================
        # РОСТ СЕКТОРОВ
        # ==================================================

        sectors_growth = analysis.get(

            "sectors_growth",

            []

        )


        if sectors_growth:


            for index, item in enumerate(

                    sectors_growth,

                    start=1

            ):


                sector = item.get(

                    "sector",

                    "Неизвестно"

                )


                change = item.get(

                    "change_percent",

                    0

                )


                text += (

                    f"{index}. "
                    f"{sector}\n"

                    f"Рост: "
                    f"{change:+.2f}%\n"

                )


        else:


            text += (

                "Нет данных\n"

            )



        text += (

            "\n"

            f"📉 ТОП 5 падения за {period} дней:\n\n"

        )



        # ==================================================
        # ПАДЕНИЕ СЕКТОРОВ
        # ==================================================

        sectors_fall = analysis.get(

            "sectors_fall",

            []

        )


        if sectors_fall:


            for index, item in enumerate(

                    sectors_fall,

                    start=1

            ):


                sector = item.get(

                    "sector",

                    "Неизвестно"

                )


                change = item.get(

                    "change_percent",

                    0

                )


                text += (

                    f"{index}. "
                    f"{sector}\n"

                    f"Падение: "
                    f"{change:+.2f}%\n"

                )


        else:


            text += (

                "Нет данных\n"

            )


        return text