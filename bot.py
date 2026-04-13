from pyrogram import Client, filters
from pyrogram.types import Message
from config import *
from database import save_file, get_file, add_user, get_all_users, total_users
from keep_alive import keep_alive

app = Client(
    "filelinkbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# START + LINK HANDLER
@app.on_message(filters.command("start"))
async def start(client, message: Message):
    user_id = message.from_user.id
    await add_user(user_id)

    if len(message.command) > 1:
        file_unique_id = message.command[1]
        data = await get_file(file_unique_id)

        if not data:
            return await message.reply_text("❌ File not found.")

        return await message.reply_cached_media(data["file_id"])

    await message.reply_text("Welcome To Luffy Store Bot\n\nOwner : @Mr_Mohammed_29")

# OWNER UPLOAD ONLY
@app.on_message(
    (filters.document | filters.video | filters.audio) &
    filters.user(OWNER_ID)
)
async def save_media(client, message: Message):
    file = message.document or message.video or message.audio

    file_id = file.file_id
    file_unique_id = file.file_unique_id

    await save_file(file_id, file_unique_id)

    link = f"https://t.me/{BOT_USERNAME}?start={file_unique_id}"

    await message.reply_text(f"🔗 Link:\n{link}")

# BLOCK OTHERS
@app.on_message(
    (filters.document | filters.video | filters.audio) &
    ~filters.user(OWNER_ID)
)
async def block_users(client, message: Message):
    await message.reply_text("❌ Only owner can upload files.")

# STATS
@app.on_message(filters.command("stats") & filters.user(OWNER_ID))
async def stats(client, message: Message):
    total = await total_users()
    await message.reply_text(f"📊 Users: {total}")

# BROADCAST
@app.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def broadcast(client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("Reply to message to broadcast.")

    msg = message.reply_to_message
    users = get_all_users()

    sent = 0
    failed = 0

    async for user in users:
        try:
            await msg.copy(user["user_id"])
            sent += 1
        except:
            failed += 1

    await message.reply_text(f"✅ Done\nSent: {sent}\nFailed: {failed}")

# RUN
keep_alive()
app.run()
