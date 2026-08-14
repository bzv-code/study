from maxapi import Router
from maxapi.types import MessageCallback


router = Router()


print("DEBUG EVENTS LOADED")


@router.message_callback()
async def debug_callback(
        event: MessageCallback
):

    print("==============================")
    print("🔥 DEBUG CALLBACK")
    print("==============================")

    print(
        "PAYLOAD:",
        event.callback.payload
    )

    print(
        "CHAT:",
        event.chat.chat_id
    )

    print(
        "USER:",
        event.from_user.user_id
    )