from pathlib import Path
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from app.repositories.moex_quotes_repository import (
    MoexQuotesRepository
)


print(
    "TICKER CHART SERVICE LOADED"
)


class TickerChartService:


    def __init__(self):

        self.repository = MoexQuotesRepository()

        self.chart_dir = Path(
            "data/charts"
        )

        self.chart_dir.mkdir(
            parents=True,
            exist_ok=True
        )


    # ==================================================
    # Удаление старых временных графиков
    # ==================================================

    def cleanup_old_charts(self):

        now = datetime.now()

        for file in self.chart_dir.glob("chart_*.png"):

            try:

                modified = datetime.fromtimestamp(
                    file.stat().st_mtime
                )

                if now - modified > timedelta(days=1):

                    file.unlink(
                        missing_ok=True
                    )

                    print(
                        f"OLD CHART REMOVED: {file.name}"
                    )

            except Exception as e:

                print(
                    f"CLEANUP ERROR: {e}"
                )


    # ==================================================
    # Создание графика
    # ==================================================

    async def create_price_chart(
            self,
            ticker: str,
            limit: int = 30
    ):

        print(
            "CHART SERVICE:",
            ticker
        )


        # чистим старые файлы

        self.cleanup_old_charts()


        history = self.repository.get_history(

            ticker=ticker,

            limit=limit

        )


        if not history:

            print(
                "NO HISTORY"
            )

            return None


        dates = []
        prices = []


        for row in history:

            dates.append(
                row["date"]
            )

            prices.append(
                row["close"]
            )


        # ClickHouse -> ASC

        dates.reverse()
        prices.reverse()


        plt.figure(
            figsize=(10, 5)
        )


        plt.plot(

            dates,

            prices,

            marker="o",

            linewidth=2

        )


        plt.title(
            f"{ticker} - цена закрытия"
        )

        plt.xlabel(
            "Дата"
        )

        plt.ylabel(
            "Цена ₽"
        )

        plt.grid(True)


        plt.gca().xaxis.set_major_formatter(

            mdates.DateFormatter("%d.%m")

        )


        plt.xticks(
            rotation=45
        )


        if prices:

            plt.annotate(

                f"{prices[-1]} ₽",

                xy=(

                    dates[-1],

                    prices[-1]

                ),

                xytext=(10, 10),

                textcoords="offset points"

            )


        plt.tight_layout()


        # ==================================================
        # Уникальное имя файла
        # ==================================================

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )


        file_path = (

            self.chart_dir /

            f"chart_{ticker}_{timestamp}.png"

        )


        plt.savefig(

            file_path,

            dpi=200,

            bbox_inches="tight"

        )


        plt.close()


        print(
            "CHART CREATED:",
            file_path
        )


        return str(file_path)