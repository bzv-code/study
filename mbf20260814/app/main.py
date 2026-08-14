import asyncio


from app.bot.client import bot

from app.core.dispatcher import dp

from app.core.lifecycle import (
    alert_monitor
)



# ==================================================
# DEBUG ROUTERS
# ==================================================

for router in dp.routers:

    print(
        "ROUTER:",
        router
    )

    for handler in router.event_handlers:

        print(
            "HANDLER:",
            handler.func_event.__name__
        )

        print(
            "STATES:",
            handler.states
        )

        print(
            "STATE FILTER:",
            handler.state_filter
        )



# ==================================================
# MAIN
# ==================================================

async def main():


    print("==============================")
    print("🚀 MAX FINAM BOT START")
    print("==============================")



    print(
        "START ALERT PRICE MONITOR"
    )


    await alert_monitor.start()



    print(
        "ROUTERS:"
    )


    for router in dp.routers:

        print(
            "ROUTER:",
            getattr(
                router,
                "router_id",
                None
            )
        )


        print(
            "HANDLERS:",
            len(
                router.event_handlers
            )
        )


        for handler in router.event_handlers:

            print(
                "  ->",
                handler.func_event.__name__,
                handler.update_type
            )



    print(
        "=============================="
    )



    try:


        await dp.start_polling(
            bot
        )


    finally:


        print(
            "STOP ALERT PRICE MONITOR"
        )


        await alert_monitor.stop()



# ==================================================
# ENTRY POINT
# ==================================================

if __name__ == "__main__":


    asyncio.run(
        main()
    )