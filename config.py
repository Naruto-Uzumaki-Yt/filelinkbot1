# ------------------------- #
# Don't Remove Credit 
# Ask Doubt @AU_Bot_Discussion 
# Owner @Mr_Mohammed_29 
# ------------------------- #

import os

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# ------------------------- #
# Don't Remove Credit 
# Ask Doubt @AU_Bot_Discussion 
# Owner @Mr_Mohammed_29 
# ------------------------- #

MONGO_URI = os.getenv("MONGO_URI")

BOT_USERNAME = os.getenv("BOT_USERNAME")  # without @

CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

# ------------------------- #
# Don't Remove Credit 
# Ask Doubt @AU_Bot_Discussion 
# Owner @Mr_Mohammed_29 
# ------------------------- #

OWNER_ID = os.getenv("OWNER_ID")
if OWNER_ID:
    OWNER_ID = int(OWNER_ID)
else:
    raise Exception("OWNER_ID is not set in environment variables")

PORT = int(os.getenv("PORT", 10000))

# ------------------------- #
# SAFETY FIX ADDED (IMPORTANT)
# ------------------------- #

# Validate required variables (prevents silent crash)
if not API_HASH:
    raise Exception("API_HASH is not set in environment variables")

if not BOT_TOKEN:
    raise Exception("BOT_TOKEN is not set in environment variables")

if not MONGO_URI:
    raise Exception("MONGO_URI is not set in environment variables")

if not BOT_USERNAME:
    raise Exception("BOT_USERNAME is not set in environment variables")

if not CHANNEL_ID:
    raise Exception("CHANNEL_ID is not set in environment variables")

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #
