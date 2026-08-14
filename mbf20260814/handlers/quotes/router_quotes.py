from maxapi import Router


from app.handlers.quotes.ticker_quotes import router as ticker_router



router = Router()



router.include_router(
    ticker_router
)



print(
    "QUOTES ROUTER LOADED"
)