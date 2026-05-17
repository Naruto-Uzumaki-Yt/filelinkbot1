from pyrogram import Client, filters
from pyrogram.types import Message
from config import API_ID, API_HASH

CLONES = {}

async def start_clone(user_id, bot_token):

    if user_id in CLONES:
        raise Exception("Clone already exists")

    clone_app = Client(
        f"clone_{user_id}",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=bot_token,
        no_updates=False
    )

    @clone_app.on_message(filters.command("start"))
    async def start_handler(client, message: Message):

        await message.reply_text(
            "✅ Clone Bot Working Successfully"
        )

    await clone_app.start()

    me = await clone_app.get_me()

    CLONES[user_id] = clone_app

    return me.username


async def stop_clone(user_id):

    if user_id not in CLONES:
        return

    bot = CLONES[user_id]

    await bot.stop()

    del CLONES[user_id]
