from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI

client = AsyncIOMotorClient(MONGO_URI)
db = client.filebot

files = db.files
users = db.users

# NEW COLLECTIONS (ADDED)
admins = db.admins
banned = db.banned


# FILES
async def save_file(file_id, file_unique_id, file_type, caption):
    await files.update_one(
        {"file_unique_id": file_unique_id},
        {"$set": {
            "file_id": file_id,
            "file_unique_id": file_unique_id,
            "file_type": file_type,
            "caption": caption
        }},
        upsert=True
    )
    
async def get_file(file_unique_id):
    return await files.find_one({"file_unique_id": file_unique_id})


# USERS
async def add_user(user_id):
    if not user_id:
        return

    await users.update_one(
        {"user_id": int(user_id)},
        {"$setOnInsert": {"user_id": int(user_id)}},
        upsert=True
    )


async def get_all_users():
    users_list = []
    async for user in users.find():
        users_list.append(user["user_id"])
    return users_list
    

async def total_users():
    return await users.count_documents({})


# =========================
# ADMIN SYSTEM (ADDED)
# =========================

async def add_admin(user_id):
    await admins.update_one(
        {"user_id": int(user_id)},
        {"$set": {"user_id": int(user_id)}},
        upsert=True
    )


async def remove_admin(user_id):
    await admins.delete_one({"user_id": int(user_id)})


async def get_admins():
    return [i["user_id"] async for i in admins.find()]


async def is_admin(user_id):
    user = await admins.find_one({"user_id": int(user_id)})
    return bool(user)


# =========================
# BAN SYSTEM (ADDED)
# =========================

async def ban_user(user_id):
    await banned.update_one(
        {"user_id": int(user_id)},
        {"$set": {"user_id": int(user_id)}},
        upsert=True
    )


async def unban_user(user_id):
    await banned.delete_one({"user_id": int(user_id)})


async def is_banned(user_id):
    user = await banned.find_one({"user_id": int(user_id)})
    return bool(user)


async def total_banned():
    return await banned.count_documents({})
