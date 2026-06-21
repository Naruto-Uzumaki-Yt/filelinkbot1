# ------------------------- #
# Don't Remove Credit 
# Ask Doubt @AU_Bot_Discussion 
# Owner @Mr_Mohammed_29 
# ------------------------- #

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import *
from pyrogram.types import InputMediaPhoto
from pyrogram.enums import ParseMode
from pyrogram.errors import FloodWait

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

import os
import sys
import platform
import random
import psutil
import time
import asyncio 
import traceback

import logging
logging.basicConfig(level=logging.INFO)

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

IMAGES = [
    "https://graph.org/file/98245197c3a4185b49dbe-3df65fb012e4195cff.jpg",
    "https://graph.org/file/27dd5451f160ce28dadd4-8ca0a7d6480451adc8.jpg",
    "https://graph.org/file/0e77ba48a8b7a3b09296f-362372bee0d84fd217.jpg"
]
from database import (
    save_file, get_file, add_user, get_all_users, total_users,
    add_admin_db, remove_admin_db, is_admin, get_all_admins
)

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

from keep_alive import keep_alive

START_TIME = time.time()
BOT_VERSION = "v3.0"

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

app = Client(
    "filelinkbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
) 

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

import base64
import re

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

BATCH_USERS = {}

# ================= GET MESSAGE ID =================

async def get_message_id(client, link):
    try:
        link = link.strip()

        if "/c/" in link:
            parts = link.split("/")
            chat_id = int("-100" + parts[-2])
            msg_id = int(parts[-1])
            
            await client.get_chat(chat_id)
            
            return chat_id, msg_id

        if "t.me/" in link:
            match = re.search(r"t\.me/([^/]+)/(\d+)", link)
            if match:
                username = match.group(1)
                msg_id = int(match.group(2))

                chat = await client.get_chat(username)
                return chat.id, msg_id

        return None, None

    except Exception:
        return None, None

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

# ================= BATCH COMMAND =================

@app.on_message(filters.command("batch") & filters.private)
async def batch_command(client, message):

    user_id = message.from_user.id

    if user_id != OWNER_ID and not await is_admin(user_id):

        return await message.reply_text(
            " ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴍʏ ᴍᴀsᴛᴇʀ. ɢᴏ ᴀᴡᴀʏ, ʙɪᴛᴄʜ 🙃."
        )

    BATCH_USERS[user_id] = {
        "step": "first"
    }

    await message.reply_text(
        "🔗 Gɪᴠᴇ Mᴇ Bᴀᴛᴄʜ Fɪʀsᴛ Mᴇssᴀɢᴇ 𝗟𝗶𝗻𝗸 ғʀᴏᴍ ʏᴏᴜʀ 𝗗𝗕 ᴄʜᴀɴɴᴇʟ"
    )

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

# ================= HANDLE BATCH =================

@app.on_message(
    filters.private &
    filters.text &
    ~filters.command([
        "start",
        "batch",
        "stats",
        "broadcast",
        "addadmin",
        "removeadmin",
        "adminlist",
        "alive",
        "id",
        "system"
    ])
)

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

async def handle_batch(client, message):

    user_id = message.from_user.id

    if user_id not in BATCH_USERS:
        return

    data = BATCH_USERS[user_id]

    # FIRST LINK
    if data["step"] == "first":

        chat_id, first_msg_id = await get_message_id(
            client,
            message.text
        )

        if not first_msg_id:

            return await message.reply_text(
                "‼️ Iɴᴠᴀʟɪᴅ Fɪʀsᴛ Lɪɴᴋ"
            )

        data["chat_id"] = chat_id
        data["first_msg_id"] = first_msg_id
        data["step"] = "last"

        return await message.reply_text(
            "🔗 Gɪᴠᴇ Mᴇ Bᴀᴛᴄʜ Lᴀsᴛ Mᴇssᴀɢᴇ 𝗟𝗶𝗻𝗸 ғʀᴏᴍ ʏᴏᴜʀ 𝗗𝗕 ᴄʜᴀɴɴᴇʟ"
        )

    # LAST LINK
    elif data["step"] == "last":

        chat_id, last_msg_id = await get_message_id(
            client,
            message.text
        )

        if not last_msg_id:

            return await message.reply_text(
                "‼️ Iɴᴠᴀʟɪᴅ Lᴀsᴛ Lɪɴᴋ"
            )

        first_msg_id = data["first_msg_id"]

        if last_msg_id < first_msg_id:

            return await message.reply_text(
                "‼️ Lᴀsᴛ ᴍᴇssᴀɢᴇ ᴍᴜsᴛ ʙᴇ ɢʀᴇᴀᴛᴇʀ ᴛʜᴀɴ ғɪʀsᴛ ᴍᴇssᴀɢᴇ"
            )

        batch_data = (
            f"batch:{data['chat_id']}:{first_msg_id}:{last_msg_id}"
        )

        encoded = base64.urlsafe_b64encode(
            batch_data.encode("utf-8")
        ).decode("utf-8")

        bot_username = (await client.get_me()).username

        link = f"https://t.me/{bot_username}?start={encoded}"

        await message.reply_text(
            f"✅ ʙᴀᴛᴄʜ ʟɪɴᴋs ɢᴇɴᴇʀᴀᴛᴇᴅ\n\n{link}"
        )

        del BATCH_USERS[user_id]
        
# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #
# START + LINK HANDLER

@app.on_message(filters.command("start"))
async def start(client, message: Message):

    user_id = message.from_user.id
    await add_user(message.from_user.id)

    # START ANIMATION
    m = await message.reply_text("ᴍᴏɴᴋᴇʏ ᴅ ʟᴜғғʏ\nɢᴇᴀʀ 𝟻. . .")
    await asyncio.sleep(0.5)
    await m.edit_text("🔥")
    await asyncio.sleep(0.5)
    await m.edit_text("⚡")
    await asyncio.sleep(0.5)
    await m.edit_text("sᴜɴ ɢᴏᴅ ɴɪᴋᴀ!...")
    await asyncio.sleep(0.5)
    await m.delete()

    if len(message.command) > 1:
        param = message.command[1]

        # ================= BATCH LINK =================

        try:
            decoded = base64.urlsafe_b64decode(
                param + "=" * (-len(param) % 4)
            ).decode("utf-8", errors="ignore")

            if not decoded.startswith("batch:"):
                raise Exception("Not batch link")

            _, chat_id, first_id, last_id = decoded.split(":")
    
            chat_id = int(chat_id)
            first_id = int(first_id)
            last_id = int(last_id)

            sent_messages = []

            wait = await message.reply_text("⏳ sᴇɴᴅɪɴɢ ғɪʟᴇs...")

            for msg_id in range(first_id, min(last_id + 1, first_id + 500)):
                try:
                    msg = await client.get_messages(chat_id, msg_id)

                    if not msg:
                        continue

                    original_caption = msg.caption or ""

                    caption = (
                        f"**{original_caption}**\n\n"
                        f"**›› Cʜᴀɴɴᴇʟ :** [Anime Updates AU](https://t.me/Anime_UpdatesAU)"
                    )

                    buttons = InlineKeyboardMarkup(
                        [[InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇs", url="https://t.me/Anime_UpdatesAU")]]
                    )

                    sent = None

                    if msg.video:
                        sent = await message.reply_video(msg.video.file_id, caption=caption, reply_markup=buttons)

                    elif msg.audio:
                        sent = await message.reply_audio(msg.audio.file_id, caption=caption, reply_markup=buttons)

                    elif msg.document:
                        sent = await message.reply_document(msg.document.file_id, caption=caption, reply_markup=buttons)

                    elif msg.sticker:
                        sent = await message.reply_sticker(msg.sticker.file_id)

                    elif msg.animation:
                        sent = await message.reply_animation(msg.animation.file_id, caption=caption, reply_markup=buttons)

                    else:
                        continue

                    sent_messages.append(sent)
                    await asyncio.sleep(0.3)

                except Exception as e:
                     print(f"Bᴀᴛᴄʜ Sᴇɴᴅ Eʀʀᴏʀ: {e}")

            await wait.delete()

            # ⏳ AUTO DELETE (ONLY IF MESSAGE SENT)
            warn = await message.reply_text(
                "⏳ Dᴜᴇ ᴛᴏ ᴄᴏᴘʏʀɪɢʜᴛ ɪssᴜᴇs...\n\n"
                "›› Yᴏᴜʀ ғɪʟᴇs ᴡɪʟʟ ʙᴇ ᴅᴇʟᴇᴛᴇᴅ ɪɴ 5 ᴍɪɴᴜᴛᴇs.\n"
                "›› Sᴏ ᴘʟᴇᴀsᴇ ғᴏʀᴡᴀʀᴅ ᴛʜᴇᴍ ᴛᴏ ᴀɴʏ ᴏᴛʜᴇʀ ᴘʟᴀᴄᴇ ғᴏʀ ғᴜᴛᴜʀᴇ ᴀᴠᴀɪʟᴀʙɪʟɪᴛʏ.\n"
                "›› ɴᴏᴛᴇ : ᴜsᴇ 𝗩𝗟𝗖 ᴘʟᴀʏᴇʀ ᴏʀ 𝗠𝗫 ᴘʟᴀʏᴇʀ  ᴛᴏ ᴡᴀᴛᴄʜ ᴛʜᴇ ᴇᴘɪsᴏᴅᴇs ᴡɪᴛʜ ɢᴏᴏᴅ ᴇxᴘᴇʀɪᴇɴᴄᴇ !."
            )

            await asyncio.sleep(300)
 
            for x in sent_messages:
                try:
                    await x.delete()
                except:
                    pass

            try:
                await warn.delete()
            except:
                pass

            return


        except Exception as e:
            print(f"Bᴀᴛᴄʜ Sʏsᴛᴇᴍ Eʀʀᴏʀ: {e}")
            
            # fallback → single file mode
            file_unique_id = message.command[1]
            data = await get_file(file_unique_id)

            if not data:
                return await message.reply_text("🔎 Fɪʟᴇ Is Nᴏᴛ Fᴏᴜɴᴅ, Cᴏɴᴛᴀᴄᴛ Tᴏ Oᴡɴᴇʀ.")

            original_caption = data.get("caption", "")

            caption = (
                f"**{original_caption}**\n\n"
                f"**›› Cʜᴀɴɴᴇʟ :** [Anime Updates AU](https://t.me/Anime_UpdatesAU)"
            )

            buttons = InlineKeyboardMarkup(
                [[InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇs", url="https://t.me/Anime_UpdatesAU")]]
            )

            sent = None

            if data.get("file_type") == "video":
                sent = await message.reply_video(data["file_id"], caption=caption, reply_markup=buttons)

            elif data.get("file_type") == "audio":
                sent = await message.reply_audio(data["file_id"], caption=caption, reply_markup=buttons)

            elif data.get("file_type") == "document":
                sent = await message.reply_document(data["file_id"], caption=caption, reply_markup=buttons)

            elif data.get("file_type") == "sticker":
                sent = await message.reply_sticker(data["file_id"])

            elif data.get("file_type") == "animation":
                sent = await message.reply_animation(data["file_id"], caption=caption, reply_markup=buttons)

            else:
                return await message.reply_text("‼️ Unsupported format")

            warn = await message.reply_text(
                "⏳ Dᴜᴇ ᴛᴏ ᴄᴏᴘʏʀɪɢʜᴛ ɪssᴜᴇs...\n\n"
                "›› Yᴏᴜʀ ғɪʟᴇs ᴡɪʟʟ ʙᴇ ᴅᴇʟᴇᴛᴇᴅ ɪɴ 5 ᴍɪɴᴜᴛᴇs.\n"
                "›› Sᴏ ᴘʟᴇᴀsᴇ ғᴏʀᴡᴀʀᴅ ᴛʜᴇᴍ ᴛᴏ ᴀɴʏ ᴏᴛʜᴇʀ ᴘʟᴀᴄᴇ ғᴏʀ ғᴜᴛᴜʀᴇ ᴀᴠᴀɪʟᴀʙɪʟɪᴛʏ.\n"
                "›› ɴᴏᴛᴇ : ᴜsᴇ 𝗩𝗟𝗖 ᴘʟᴀʏᴇʀ ᴏʀ 𝗠𝗫 ᴘʟᴀʏᴇʀ  ᴛᴏ ᴡᴀᴛᴄʜ ᴛʜᴇ ᴇᴘɪsᴏᴅᴇs ᴡɪᴛʜ ɢᴏᴏᴅ ᴇxᴘᴇʀɪᴇɴᴄᴇ !."
            )

            m2 = await message.reply_text("ᴍᴏɴᴋᴇʏ ᴅ ʟᴜғғʏ...")
            await asyncio.sleep(0.4)
            await m2.edit_text("sᴜɴ ɢᴏᴅ ɴɪᴋᴀ...")
            await asyncio.sleep(0.5)
            await m2.delete()

            await asyncio.sleep(300)

            try:
                if sent:
                    await sent.delete()
                await warn.delete()
            except:
                pass

            return

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

# ONLY OWNER + ADMIN CAN UPLOAD 
@app.on_message(
    (filters.document | filters.video | filters.audio | filters.sticker | filters.animation) &
    filters.private
)
async def save_media(client, message: Message):

    # Allow only owner + admin
    if not (message.from_user.id == OWNER_ID or await is_admin(message.from_user.id)):
        return await message.reply_text("ғᴜᴄᴋ ʏᴏᴜ, ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴍʏ ᴍᴀsᴛᴇʀ. ɢᴏ ᴀᴡᴀʏ, ʙɪᴛᴄʜ 🙃..")

    original_caption = message.caption if message.caption else ""

    # Detect file type
    if message.video:
        file = message.video
        file_type = "video"
        thumb = None
        if hasattr(file, "thumbs") and file.thumbs:
            thumb = file.thumbs[-1].file_id

    elif message.audio:
        file = message.audio
        file_type = "audio"
        thumb = None

    elif message.document:
        file = message.document
        file_type = "document"
        thumb = None

    elif message.sticker:
        file = message.sticker
        file_type = "sticker"
        thumb = None

    elif message.animation:  # GIF
        file = message.animation
        file_type = "animation"
        thumb = None

    else:
        return await message.reply_text("‼️ Uɴsᴜᴘᴘᴏʀᴛᴇᴅ Fᴏʀᴍᴀᴛ")

    file_id = file.file_id
    file_unique_id = file.file_unique_id

    await save_file(file_id, file_unique_id, file_type, original_caption, thumb)

    link = f"https://t.me/{BOT_USERNAME}?start={file_unique_id}"

    await message.reply_text(f"🔗 𝗛𝗲𝗿𝗲 𝗜𝘀 𝗬𝗼𝘂𝗿 𝗟𝗶𝗻𝗸:\n{link}")
    
# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #
# STATS
@app.on_message(filters.command("stats") & filters.user(OWNER_ID))
async def stats(client, message: Message):

    start = time.time()
    total = await total_users()

    uptime_seconds = int(time.time() - START_TIME)
    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    ping = round((time.time() - start) * 1000)

    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🔄 Rᴇғʀᴇsʜ", callback_data="refresh_stats")]]
    )

    process = psutil.Process()
    memory = process.memory_info().rss / (1024 * 1024)

    await message.reply_text(
        f"📊 **𝗕𝗼𝘁 𝗦𝘁𝗮𝘁𝘂𝘀**\n\n"
        f"👥 Usᴇʀs: {total}\n"
        f"⏱ Uᴘᴛɪᴍᴇ: {hours}h {minutes}m {seconds}s\n"
        f"⚡ Pɪɴɢ: {ping} ms\n"
        f"🧠 Mᴇᴍᴏʀʏ Usᴀɢᴇ: {memory:.2f} MB\n"
        f"🧾 Vᴇʀsɪᴏɴ: {BOT_VERSION}",
        reply_markup=keyboard
    )

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

# BROADCAST
@app.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def broadcast(client, message: Message):

    if not message.reply_to_message:
        return await message.reply_text("Rᴇᴘʟʏ Tᴏ A Mᴇssᴀɢᴇ Tᴏ Bʀᴏᴀᴅᴄᴀsᴛ..")

    msg = message.reply_to_message

    users = await get_all_users()

    sent = 0
    failed = 0

    status = await message.reply_text("⏳️ 𝗕𝗿𝗼𝗮𝗱𝗰𝗮𝘀𝘁 𝗦𝘁𝗮𝗿𝘁𝗲𝗱.....")  

    for user_id in users:
        try:
            await msg.copy(chat_id=int(user_id))
            sent += 1
            await asyncio.sleep(0.2)

        except FloodWait as e:
            await asyncio.sleep(e.value)

        except Exception as e:
            failed += 1
            print(f"Failed: {user_id} | {e}")

    await status.edit_text(
        f"⏳️ 𝗕𝗿𝗼𝗮𝗱𝗰𝗮𝘀𝘁 𝗖𝗼𝗺𝗽𝗹𝗲𝘁𝗲𝗱\n\n"
        f"◇ Sᴜᴄᴄᴇssғᴜʟ: {sent}\n"
        f"◇ Uɴsᴜᴄᴄᴇssғᴜʟ: {failed}"
    )
    
# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #
@app.on_message(
    filters.private &
    ~filters.service &
    ~filters.command([
        "start",
        "batch",
        "stats",
        "broadcast",
        "addadmin",
        "removeadmin",
        "adminlist",
        "alive",
        "id",
        "system"
    ])
)
async def auto_add_user(client, message):
    if message.from_user:
        await add_user(message.from_user.id)
        
# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

# ADD ADMIN 
@app.on_message(filters.command("addadmin") & filters.private)
async def add_admin(client, message: Message):

    if message.from_user.id != OWNER_ID:
        return await message.reply_text("ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴍʏ ᴍᴀsᴛᴇʀ. ɢᴏ ᴀᴡᴀʏ, ʙɪᴛᴄʜ 🙃..")

    if len(message.command) < 2:
        return await message.reply_text("ʀᴇᴘʟʏ ᴛᴏ /addadmin user_id")

    try:
        user_id = int(message.command[1])
    except:
        return await message.reply_text("‼️ ɪɴᴠᴀʟɪᴅ ᴜsᴇʀ ɪᴅ")

    user = await client.get_users(user_id)

    name = user.first_name
    username = user.username if user.username else "None"

    await add_admin_db(user_id, name, username)

    await message.reply_text(f"✅️ ᴀᴅᴍɪɴ ɪs ᴀᴅᴅᴇᴅ : {user_id}")

    # Send message to that user
    try:
        await client.send_message(
            chat_id=user_id,
            text="🎉 ᴄᴏɴɢʀᴀᴛᴜʟᴀᴛɪᴏɴs ʏᴏᴜ ʜᴀᴠᴇ ʙᴇᴇɴ ᴘʀᴏᴍᴏᴛᴇᴅ ᴛᴏ 𝗔𝗗𝗠𝗜𝗡\n\nYᴏᴜ ᴄᴀɴ ɴᴏᴡ ᴜᴘʟᴏᴀᴅ ғɪʟᴇs ᴛᴏ ᴛʜᴇ ʙᴏᴛ ᴀɴᴅ ɢᴇɴᴇʀᴀᴛᴇ ʟɪɴᴋs."
        )
    except Exception as e:
        print(f"Fᴀɪʟᴇᴅ Tᴏ Nᴏᴛɪғʏ Aᴅᴍɪɴ : {e}")
        
# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

# REMOVE ADMIN 
@app.on_message(filters.command("removeadmin") & filters.private)
async def remove_admin(client, message: Message):

    if message.from_user.id != OWNER_ID:
        return await message.reply_text("ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴍʏ ᴍᴀsᴛᴇʀ. ɢᴏ ᴀᴡᴀʏ, ʙɪᴛᴄʜ 🙃..")

    if len(message.command) < 2:
        return await message.reply_text("ʀᴇᴘʟʏ ᴛᴏ /removeadmin user_id")

    try:
        user_id = int(message.command[1])
    except:
        return await message.reply_text("‼️ ɪɴᴠᴀʟɪᴅ ᴜsᴇʀ ɪᴅ")

    await remove_admin_db(user_id)

    await message.reply_text(f"✅️ ᴀᴅᴍɪɴ ɪs ʀᴇᴍᴏᴠᴇᴅ : {user_id}")
    
# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

#ADMIN LIST
@app.on_message(filters.command("adminlist") & filters.private)
async def admin_list(client, message: Message):

    if message.from_user.id != OWNER_ID:
        return await message.reply_text("🚫 𝗬𝗼𝘂 𝗔𝗿𝗲 𝗡𝗼𝘁 𝗔𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗲𝗱 𝗧𝗼 𝗨𝘀𝗲 𝗧𝗵𝗶𝘀 𝗖𝗼𝗺𝗺𝗮𝗻𝗱")

    admins = await get_all_admins()

    if not admins:
        return await message.reply_text("‼️ Nᴏ Aᴅᴍɪɴs Fᴏᴜɴᴅ Iɴ Lɪsᴛ")

    text = "👑 Aᴅᴍɪɴ Lɪsᴛ\n\n"

    for i, admin in enumerate(admins, start=1):
        name = admin.get("name", "Unknown")
        username = admin.get("username", "None")
        user_id = admin.get("user_id")

        text += (
            f"{i}. 𝗡𝗮𝗺𝗲: {name}\n"
            f"   𝗨𝘀𝗲𝗿𝗻𝗮𝗺𝗲: @{username if username != 'None' else 'no_username'}\n"
            f"   𝗜𝗗: {user_id}\n\n"
        )

    await message.reply_text(text)
    
# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

# ABOUT HANDLER
@app.on_callback_query(filters.regex("about"))
async def about_callback(client, query):
    await query.message.edit_text(
        "⍟───[ MY ᴅᴇᴛᴀɪʟꜱ ]───⍟\n\n"
        "‣ ᴍʏ ɴᴀᴍᴇ : [ᴀᴜ ʟᴜғғʏ sᴛᴏʀᴇ ʙᴏᴛ](https://t.me/AU_Luffy_Store_bot)\n"
        "‣ ᴅᴇᴠᴇʟᴏᴘᴇʀ : [ᴍᴏʜᴀᴍᴍᴇᴅ](https://t.me/Mr_Mohammed_29)\n"
        "‣ ʟɪʙʀᴀʀʏ : [ᴘʏʀᴏɢʀᴀᴍ 𝟸.𝟶](https://pypi.org/project/Pyrogram/)\n"
        "‣ ʟᴀɴɢᴜᴀɢᴇ : [ᴘʏᴛʜᴏɴ 𝟹](https://www.python.org/downloads/)\n"
        "‣ ᴅᴀᴛᴀ ʙᴀsᴇ : [ᴍᴏɴɢᴏ ᴅʙ](https://www.mongodb.com/)\n"
        "‣ ʙᴏᴛ sᴇʀᴠᴇʀ : [Bᴏᴛs Sᴇʀᴠᴇʀ](https://render.com)\n"
        "‣ ᴜᴘᴅᴀᴛᴇs : [ᴀɴɪᴍᴇ ᴜᴘᴅᴀᴛᴇs](https://t.me/Anime_UpdatesAU)\n"
        "‣ ʙᴜɪʟᴅ sᴛᴀᴛᴜs : ᴠ3.𝟶 [sᴛᴀʙʟᴇ](https://t.me/Anime_UpdatesAU)",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("ʜᴏᴍᴇ", callback_data="home")]]
        ),
        parse_mode=ParseMode.MARKDOWN
    )

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

# HOME HANDLER
@app.on_callback_query(filters.regex("home"))
async def home_callback(client, query):

    photo = random.choice(IMAGES)

    await query.message.edit_media(
        media=InputMediaPhoto(
            media=photo,
            caption=(
                "𝗛𝗲𝗹𝗹𝗼 ♡,\n\n"
                "›› 𝗜 𝗰𝗮𝗻 𝘀𝘁𝗼𝗿𝗲 𝗽𝗿𝗶𝘃𝗮𝘁𝗲 𝗳𝗶𝗹𝗲𝘀 𝗶𝗻 𝗦𝗽𝗲𝗰𝗶𝗳𝗶𝗲𝗱 𝗖𝗵𝗮𝗻𝗻𝗲𝗹 𝗮𝗻𝗱 𝗼𝘁𝗵𝗲𝗿 𝘂𝘀𝗲𝗿𝘀 𝗰𝗮𝗻 𝗮𝗰𝗰𝘀𝘀 𝗶𝘁 𝗳𝗿𝗼𝗺 𝘀𝗽𝗲𝗰𝗶𝗮𝗹 𝗹𝗶𝗻𝗸."
            ),
            parse_mode=ParseMode.MARKDOWN
        ),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇs", url="https://t.me/Anime_UpdatesAU"),
                    InlineKeyboardButton("ᴀʙᴏᴜᴛ", callback_data="about")
                ],
                [
                    InlineKeyboardButton("ᴏᴡɴᴇʀ", url="https://t.me/+ssaZDrj3Wr4wNzI1")
                ]
            ]
        )
    )

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

# REFRESH STATS 
@app.on_callback_query(filters.regex("refresh_stats"))
async def refresh_stats(client, query):

    start = time.time()
    total = await total_users()

    uptime_seconds = int(time.time() - START_TIME)
    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    ping = round((time.time() - start) * 1000)

    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🔄 Rᴇғʀᴇsʜ", callback_data="refresh_stats")]]
    )

    process = psutil.Process()
    memory = process.memory_info().rss / (1024 * 1024)

    await query.message.edit_text(
        f"📊 **𝗕𝗼𝘁 𝗦𝘁𝗮𝘁𝘂𝘀**\n\n"
        f"👥 Usᴇʀs: {total}\n"
        f"⏱ Uᴘᴛɪᴍᴇ: {hours}h {minutes}m {seconds}s\n"
        f"⚡ Pɪɴɢ: {ping} ms\n"
        f"🧠 Mᴇᴍᴏʀʏ Usᴀɢᴇ: {memory:.2f} MB\n"
        f"🧾 Vᴇʀsɪᴏɴ: {BOT_VERSION}",
        reply_markup=keyboard
    )

    await query.answer("Sᴛᴀᴛs Uᴘᴅᴀᴛᴇᴅ 🔄")   

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

# ------------------------- #
# ALIVE COMMAND
# ------------------------- #

@app.on_message(filters.command("alive"))
async def alive(client, message):

    await message.reply_photo(
        photo="https://graph.org/file/ffdbc01d09855874311b1-5f3f1eae52d984db3d.jpg",
        caption=(
            "❤️ **Yᴏᴜ ᴀʀᴇ ᴠᴇʀʏ ʟᴜᴄᴋʏ 🤞 I ᴀᴍ ᴀʟɪᴠᴇ ❤️\n\n"
            "Pʀᴇss /start ᴛᴏ ᴜsᴇ ᴍᴇ!**"
        )
    )

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

# ------------------------- #
# ID COMMAND
# ------------------------- #

@app.on_message(filters.command("id"))
async def get_id(client, message):

    user = message.from_user

    text = (
        "👤 **Usᴇʀ Iɴғᴏʀᴍᴀᴛɪᴏɴ**\n\n"
        f"➲ Fɪʀsᴛ Nᴀᴍᴇ: {user.first_name or 'None'}\n"
        f"➲ Lᴀsᴛ Nᴀᴍᴇ: {user.last_name or 'None'}\n"
        f"➲ Usᴇʀɴᴀᴍᴇ: {user.username or 'None'}\n"
        f"➲ Tᴇʟᴇɢʀᴀᴍ ID: {user.id}\n"
        f"➲ Dᴀᴛᴀ Cᴇɴᴛʀᴇ: {user.dc_id or 'Unknown'}"
    )

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "👤 Vɪᴇᴡ Pʀᴏғɪʟᴇ",
                    url=f"tg://user?id={user.id}"
                )
            ]
        ]
    )

    try:
        photos = await client.get_profile_photos(
            user.id,
            limit=1
        )

        if photos:
            await message.reply_photo(
                photos[0].file_id,
                caption=text,
                reply_markup=keyboard
            )
        else:
            await message.reply_text(
                text,
                reply_markup=keyboard
            )

    except:
        await message.reply_text(
            text,
            reply_markup=keyboard
        )

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

# ------------------------- #
# SYSTEM COMMAND
# ------------------------- #

@app.on_message(filters.command("system"))
async def system_info(client, message):

    os_name = platform.system()

    uptime = int(time.time() - START_TIME)
    d, rem = divmod(uptime, 86400)
    h, rem = divmod(rem, 3600)
    m, s = divmod(rem, 60)

    sys_time = int(time.time() - psutil.boot_time())
    sd, rem = divmod(sys_time, 86400)
    sh, rem = divmod(rem, 3600)
    sm, ss = divmod(rem, 60)

    ram = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    text = (
        "💻 **Sʏsᴛᴇᴍ Iɴғᴏʀᴍᴀᴛɪᴏɴ Pᴀɴᴇʟ**\n\n"
        f"🖥️ OS Dᴇᴛᴀɪʟs: {os_name}\n"
        f"⏰ Bᴏᴛ Uᴘᴛɪᴍᴇ: {d}ᴅ : {h}ʜ : {m}ᴍ : {s}s\n"
        f"🔄 Sʏsᴛᴇᴍ Uᴘᴛɪᴍᴇ: {sd}ᴅ : {sh}ʜ : {sm}ᴍ : {ss}s\n"
        f"💾 Rᴀᴍ Usᴀɢᴇ: {ram.used/(1024**3):.2f} GB / {ram.total/(1024**3):.2f} GB\n"
        f"📁 Dɪsᴋ Usᴀɢᴇ: {disk.used/(1024**3):.2f} GB / {disk.total/(1024**3):.2f} GB"
    )

    await message.reply_text(text)

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

if __name__ == "__main__":
    keep_alive()
    print("""
╔══════════════════════════════╗
║   ᴍᴏʜᴀᴍᴍᴇᴅᴅᴇᴠ-ʏᴛ                   ║
║   ғɪʟᴇ sᴛᴏʀᴇ ʙᴏᴛ sᴛᴀʀᴛᴇᴅ.            ║
╚══════════════════════════════╝
""")
    app.run()

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #
