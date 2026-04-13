import os

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

MONGO_URI = os.getenv("MONGO_URI")

BOT_USERNAME = os.getenv("BOT_USERNAME")  # without @
OWNER_ID = int(os.getenv("OWNER_ID"))
PORT = int(os.getenv("PORT", 10000))
