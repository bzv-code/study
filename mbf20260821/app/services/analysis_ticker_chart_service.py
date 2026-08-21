from pathlib import Path
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from app.repositories.moex_quotes_repository import (
    MoexQuotesRepository
)


print(
    "ANALYSIS TICKER CHART SERVICE LOADED"
)


class AnalysisTickerChartService:


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
            ticker,
            "LIMIT:",
            limit
        )


        # чистим старые файлы

        self.cleanup_old_charts()


        # ==================================================
        # Выбор источника данных в зависимости от периода
        # ==================================================

        if limit == 1:

            # 1 день -> почасовые данные из moex_stock_h1
            history = self.repository.get_hourly_history(
                ticker=ticker,
                limit=24
            )
            date_format = "%H:%M"
            period_label = "1 день (по часам)"
            x_label = "Время"


        elif limit == 180:

            # 180 дней -> недельные данные из moex_stock_h
            history = self.repository.get_weekly_history(
                ticker=ticker,
                limit=26  # ~26 недель = полгода
            )
            date_format = "%d.%m"
            period_label = "180 дней (по неделям)"
            x_label = "Дата"


        else:

            # 7/14/30 дней -> дневные данные из moex_stock_d
            history = self.repository.get_history(
                ticker=ticker,
                limit=limit
            )
            date_format = "%d.%m"
            period_label = f"{limit} дней"
            x_label = "Дата"


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
            f"{ticker} - {period_label}"
        )

        plt.xlabel(
            x_label
        )

        plt.ylabel(
            "Цена ₽"
        )

        plt.grid(True)


        plt.gca().xaxis.set_major_formatter(

            mdates.DateFormatter(date_format)

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