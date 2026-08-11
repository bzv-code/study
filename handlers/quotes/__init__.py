# ==================================================
# КОТИРОВКИ
# ==================================================

from .ticker_quotes import (
    router as ticker_router
)



# ==================================================
# АНАЛИЗ ТИКЕТА
# ==================================================

from .analysis_ticker_quotes import (
    router as analysis_ticker_router
)



# ==================================================
# АНАЛИЗ АКЦИЙ
# ==================================================

from .analysis_stocks_quotes import (
    router as analysis_stocks_router
)



# ==================================================
# АНАЛИЗ СЕКТОРОВ
# ==================================================

from .analysis_sectors_quotes import (
    router as analysis_sectors_router
)



# ==================================================
# ПОРТФЕЛЬ
# ==================================================

from .portfolio_quotes import (
    router as portfolio_router
)


from .portfolio_add_quotes import (
    router as portfolio_add_router
)


from .portfolio_delete_quotes import (
    router as portfolio_delete_router
)


from .portfolio_sell_quotes import (
    router as portfolio_sell_router
)


from .portfolio_sell_quantity_quotes import (
    router as portfolio_sell_quantity_router
)


from .portfolio_sell_price_quotes import (
    router as portfolio_sell_price_router
)



# ==================================================
# УВЕДОМЛЕНИЯ
# ==================================================

from .alert_quotes import (
    router as alert_router
)



print(
    "QUOTES ROUTERS LOADED"
)



routers = [


    # ==========================================
    # Котировки
    # ==========================================

    ticker_router,



    # ==========================================
    # Анализ
    # ==========================================

    analysis_ticker_router,

    analysis_stocks_router,

    analysis_sectors_router,



    # ==========================================
    # Портфель
    # ==========================================

    portfolio_router,

    portfolio_add_router,

    portfolio_delete_router,

    portfolio_sell_router,

    portfolio_sell_quantity_router,

    portfolio_sell_price_router,



    # ==========================================
    # Уведомления
    # ==========================================

    alert_router

]



print(
    "QUOTE ROUTERS COUNT:",
    len(routers)
)