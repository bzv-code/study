# app/handlers/callbacks/router_callback.py


# ==================================================
# CALLBACKS
# ==================================================

# УДАЛЕНО: котировки
# from .ticker_callbacks import (
#     router as quote_router
# )


# УДАЛЕНО: история тикера из котировок
# from .ticker_history_callbacks import (
#     router as ticker_history_router
# )


# УДАЛЕНО: график из котировок
# from .chart_callbacks import (
#     router as chart_router
# )



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
# РЕЖИМ ПРОДАЖИ / ОРДЕРА
# ==================================================

from .sell_mode_callbacks import (
    router as sell_mode_router
)


from .orders_callbacks import (
    router as orders_router
)

# ==================================================
# УВЕДОМЛЕНИЯ
# ==================================================

# УДАЛЕНО: Создание уведомления из меню котировки
# from .alert_ticker_callbacks import (
#     router as alert_ticker_router
# )


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
# ДИВИДЕНДЫ
# ==================================================

from .dividends_callbacks import (
    router as dividends_router
)

# ==================================================
# ИНФОРМАЦИЯ
# ==================================================

from .info_callbacks import (
    router as info_router
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
    # УДАЛЕНО: Основные (котировки)
    # ----------------------------------------------

    # quote_router,

    # ticker_history_router,

    # chart_router,



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

    sell_mode_router,

    orders_router,

    # ----------------------------------------------
    # Уведомления
    # ----------------------------------------------

    # УДАЛЕНО: 🔔 Из меню котировки
    # alert_ticker_router,


    # 🔔 Главное меню уведомлений
    alert_router,


    # 🔼 Цена выше / 🔽 Цена ниже
    alert_condition_router,

    # ----------------------------------------------
    # Дивиденды
    # ----------------------------------------------

    dividends_router,

    # ==================================================
    # ИНФОРМАЦИЯ
    # ==================================================

    info_router,

    # ----------------------------------------------
    # Главное меню
    # ----------------------------------------------

    home_router

]



print(
    "CALLBACK ROUTERS COUNT:",
    len(routers)
)