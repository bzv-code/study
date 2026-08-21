print(
    "ANALYSIS STOCKS FORMATTER LOADED"
)


class AnalysisStocksFormatter:


    @classmethod
    def format_stocks_analysis(

            cls,

            analysis: dict

    ) -> str:


        if not analysis:

            return (
                "❌ Нет данных по акциям"
            )


        period = analysis.get(

            "period",

            7

        )


        text = (

            "🌎 Анализ акций\n\n"

            f"📈 ТОП 5 роста за {period} дней:\n\n"

        )


        # ==================================================
        # РОСТ
        # ==================================================

        stocks_growth = analysis.get(

            "stocks_growth",

            []

        )


        if stocks_growth:


            for index, item in enumerate(

                    stocks_growth,

                    start=1

            ):


                ticker = item.get(

                    "ticker",

                    ""

                )


                change = item.get(

                    "change_percent",

                    0

                )


                text += (

                    f"{index}. "
                    f"{ticker} "
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
        # ПАДЕНИЕ
        # ==================================================

        stocks_fall = analysis.get(

            "stocks_fall",

            []

        )


        if stocks_fall:


            for index, item in enumerate(

                    stocks_fall,

                    start=1

            ):


                ticker = item.get(

                    "ticker",

                    ""

                )


                change = item.get(

                    "change_percent",

                    0

                )


                text += (

                    f"{index}. "
                    f"{ticker} "
                    f"{change:+.2f}%\n"

                )


        else:


            text += (

                "Нет данных\n"

            )


        return text