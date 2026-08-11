from maxapi.filters.callback_payload import CallbackPayload



# ==================================================
# MAIN MENU
# ==================================================


class QuotePayload(
    CallbackPayload,
    prefix="quote"
):
    pass



class HistoryPayload(
    CallbackPayload,
    prefix="history"
):
    pass



class ChartPayload(
    CallbackPayload,
    prefix="chart"
):
    pass



class AnalysisPayload(
    CallbackPayload,
    prefix="analysis"
):
    """
    Главное меню анализа
    """

    pass



class PortfolioPayload(
    CallbackPayload,
    prefix="portfolio"
):
    pass



class AlertsPayload(
    CallbackPayload,
    prefix="alerts"
):
    """
    Раздел уведомлений
    """

    pass





# ==================================================
# ANALYSIS TICKER
# ==================================================


class AnalysisTickerPayload(
    CallbackPayload,
    prefix="analysis_ticker"
):
    pass



class AnalysisPeriodPayload(
    CallbackPayload,
    prefix="analysis_period"
):
    period: str





# ==================================================
# ANALYSIS STOCKS
# ==================================================


class AnalysisStocksPayload(
    CallbackPayload,
    prefix="analysis_stocks"
):
    pass



class AnalysisStocksPeriodPayload(
    CallbackPayload,
    prefix="analysis_stocks_period"
):
    period: str





# ==================================================
# ANALYSIS SECTORS
# ==================================================


class AnalysisSectorsPayload(
    CallbackPayload,
    prefix="analysis_sectors"
):
    pass



class AnalysisSectorsPeriodPayload(
    CallbackPayload,
    prefix="analysis_sectors_period"
):
    period: str





# ==================================================
# PORTFOLIO
# ==================================================


class AddPortfolioPayload(
    CallbackPayload,
    prefix="add_portfolio"
):
    pass



class AddPortfolioFromMenuPayload(
    CallbackPayload,
    prefix="portfolio_add"
):
    pass



class SellPortfolioPayload(
    CallbackPayload,
    prefix="portfolio_sell"
):
    pass



class DeletePortfolioPayload(
    CallbackPayload,
    prefix="portfolio_delete"
):
    pass



class ClearHistoryPayload(
    CallbackPayload,
    prefix="portfolio_clear_history"
):
    pass





# ==================================================
# ALERTS
# ==================================================


class CreateAlertPayload(
    CallbackPayload,
    prefix="create_alert"
):
    """
    Создание уведомления из раздела уведомлений
    """

    pass



class CreateAlertFromQuotePayload(
    CallbackPayload,
    prefix="create_alert_quote"
):
    """
    Создание уведомления из меню котировки
    """

    pass



class AlertConditionPayload(
    CallbackPayload,
    prefix="alert_condition"
):
    """
    Условие уведомления:

    above
    below
    """

    condition: str



class DeleteAlertPayload(
    CallbackPayload,
    prefix="delete_alert"
):
    """
    Удаление уведомления
    """

    alert_id: int





# ==================================================
# HOME
# ==================================================


class HomePayload(
    CallbackPayload,
    prefix="home"
):
    pass