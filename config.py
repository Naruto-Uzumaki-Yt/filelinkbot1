import os

def must_get(name):
    value = os.getenv(name)
    if not value:
        raise Exception(f"{name} is not set in environment variables")
    return value

API_ID = int(must_get("API_ID"))
API_HASH = must_get("API_HASH")
BOT_TOKEN = must_get("BOT_TOKEN")

MONGO_URI = must_get("MONGO_URI")

BOT_USERNAME = must_get("BOT_USERNAME")

CHANNEL_ID = int(must_get("CHANNEL_ID"))

OWNER_ID = int(must_get("OWNER_ID"))

PORT = int(os.getenv("PORT", "10000"))

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #
