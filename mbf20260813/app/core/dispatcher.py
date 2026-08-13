from maxapi import Dispatcher



# ==================================================
# START
# ==================================================

from app.handlers.start import (
    router as start_router
)



# ==================================================
# CALLBACKS
# ==================================================

from app.handlers.callbacks import (
    routers as callbacks_routers
)



# ==================================================
# QUOTES / MESSAGE HANDLERS
# ==================================================

from app.handlers.quotes import (
    routers as quotes_routers
)



print(
    "CALLBACK ROUTERS:",
    len(callbacks_routers)
)


print(
    "QUOTE ROUTERS:",
    len(quotes_routers)
)



# ==================================================
# DISPATCHER
# ==================================================

dp = Dispatcher()



dp.include_routers(

    # Главное меню /start

    start_router,


    # Callback кнопки

    *callbacks_routers,


    # Сообщения и состояния

    *quotes_routers

)



print(
    "DISPATCHER LOADED"
)