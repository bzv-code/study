from maxapi import Router
from maxapi.types import MessageCreated


router = Router("debug_message_router")


print("DEBUG MESSAGE ROUTER LOADED")


@router.message_created()
async def debug_message(
        event: MessageCreated
):

    print("==============================")
    print("MESSAGE EVENT")
    print("==============================")


    print(
        "CHAT ID:",
        event.message.recipient.chat_id
    )


    print(
        "USER ID:",
        event.message.sender.user_id
    )


    print(
        "TEXT:",
        event.message.body.text
        if event.message.body
        else None
    )