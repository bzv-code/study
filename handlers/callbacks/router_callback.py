# app/handlers/callbacks/router_callback.py


# ==================================================
# ОСНОВНЫЕ CALLBACKS
# ==================================================

from .ticker_callbacks import (
    router as quote_router
)


from .ticker_history_callbacks import (
    router as ticker_history_router
)


from .chart_callbacks import (
    router as chart_router
)



# ==================================================
# АНАЛИЗ
# ==================================================

from .analysis_general_callbacks import (
    router as analysis_general_router
)



# --------------------------------------------------
# Анализ тикета
# --------------------------------------------------

from .analysis_ticker_callbacks import (
    router as analysis_ticker_router
)


from .analysis_ticker_period_callbacks import (
    router as analysis_ticker_period_router
)



# --------------------------------------------------
# Анализ акций
# --------------------------------------------------

from .analysis_stocks_callbacks import (
    router as analysis_stocks_router
)


from .analysis_stocks_period_callbacks import (
    router as analysis_stocks_period_router
)



# --------------------------------------------------
# Анализ секторов
# --------------------------------------------------

from .analysis_sectors_callbacks import (
    router as analysis_sectors_router
)


from .analysis_sectors_period_callbacks import (
    router as analysis_sectors_period_router
)



# ==================================================
# ПОРТФЕЛЬ
# ==================================================

from .portfolio_callbacks import (
    router as portfolio_router
)


from .portfolio_add_callbacks import (
    router as portfolio_add_router
)


from .portfolio_delete_callbacks import (
    router as portfolio_delete_router
)


from .portfolio_sell_callbacks import (
    router as portfolio_sell_router
)


from .portfolio_clear_history_callbacks import (
    router as portfolio_clear_history_router
)



# ==================================================
# УВЕДОМЛЕНИЯ
# ==================================================

# Создание уведомления из меню котировки
from .alert_ticker_callbacks import (
    router as alert_ticker_router
)


# Главное меню уведомлений
from .alert_callbacks import (
    router as alert_router
)


# Выбор условия:
# Цена выше / Цена ниже
from .alert_condition_callbacks import (
    router as alert_condition_router
)



# ==================================================
# HOME
# ==================================================

from .general_menu_callbacks import (
    router as home_router
)



print(
    "CALLBACK ROUTER LOADED"
)



# ==================================================
# CALLBACK ROUTERS
# ==================================================

routers = [


    # ----------------------------------------------
    # Основные
    # ----------------------------------------------

    quote_router,

    ticker_history_router,

    chart_router,



    # ----------------------------------------------
    # Анализ
    # ----------------------------------------------

    analysis_general_router,


    analysis_ticker_router,

    analysis_ticker_period_router,


    analysis_stocks_router,

    analysis_stocks_period_router,


    analysis_sectors_router,

    analysis_sectors_period_router,



    # ----------------------------------------------
    # Портфель
    # ----------------------------------------------

    portfolio_router,

    portfolio_add_router,

    portfolio_delete_router,

    portfolio_sell_router,

    portfolio_clear_history_router,



    # ----------------------------------------------
    # Уведомления
    # ----------------------------------------------

    # 🔔 Из меню котировки
    alert_ticker_router,


    # 🔔 Главное меню уведомлений
    alert_router,


    # 🔼 Цена выше / 🔽 Цена ниже
    alert_condition_router,



    # ----------------------------------------------
    # Главное меню
    # ----------------------------------------------

    home_router

]



print(
    "CALLBACK ROUTERS COUNT:",
    len(routers)
)