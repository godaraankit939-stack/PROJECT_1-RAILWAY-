from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL

# Connect to MongoDB
client = AsyncIOMotorClient(MONGO_URL)
db = client["DARK_USERBOT"]

# Collections
users_col = db["hosted_users"]
sudo_col = db["sudo_users"]
ban_col = db["banned_users"]
settings_col = db["bot_settings"]
profile_col = db["original_profiles"]

# --- SESSION FUNCTIONS ---
async def save_session(user_id, session_string):
    await users_col.update_one({"user_id": user_id}, {"$set": {"session": session_string}}, upsert=True)

async def get_all_sessions():
    sessions = []
    async for user in users_col.find():
        sessions.append(user["session"])
    return sessions

# --- SUDO FUNCTIONS ---
async def add_sudo(user_id):
    await sudo_col.update_one({"user_id": user_id}, {"$set": {"user_id": user_id}}, upsert=True)

async def is_sudo(user_id):
    res = await sudo_col.find_one({"user_id": user_id})
    return True if res else False

# --- BAN FUNCTIONS ---
async def ban_user(user_id):
    await ban_col.update_one({"user_id": user_id}, {"$set": {"user_id": user_id}}, upsert=True)

async def unban_user(user_id):
    await ban_col.delete_one({"user_id": user_id})

async def is_banned(user_id):
    res = await ban_col.find_one({"user_id": user_id})
    return True if res else False

# --- MAINTENANCE FUNCTIONS ---
async def set_maintenance(state: bool):
    await settings_col.update_one({"id": "maint"}, {"$set": {"state": state}}, upsert=True)

async def get_maintenance():
    res = await settings_col.find_one({"id": "maint"})
    return res["state"] if res else False

# --- PROFILE BACKUP (For .revert) ---
async def save_original_profile(user_id, first_name, last_name, about):
    exists = await profile_col.find_one({"user_id": user_id})
    if not exists:
        await profile_col.insert_one({
            "user_id": user_id,
            "first_name": first_name,
            "last_name": last_name,
            "about": about
        })

async def get_original_profile(user_id):
    return await profile_col.find_one({"user_id": user_id})
