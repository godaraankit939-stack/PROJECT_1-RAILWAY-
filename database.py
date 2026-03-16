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

# Ye function missing tha, isliye error aaya
async def get_sudo_list():
    sudo_users = []
    async for user in sudo_col.find():
        sudo_users.append(user["user_id"])
    return sudo_users

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
    
# --- ANTIPM COLLECTIONS ---
antipm_col = db["antipm_settings"]
warns_col = db["pm_warns"]
approved_col = db["approved_users"]

# 1. AntiPM Status (On/Off)
async def set_antipm_status(state: bool):
    await antipm_col.update_one({"id": "status"}, {"$set": {"state": state}}, upsert=True)

async def get_antipm_status():
    res = await antipm_col.find_one({"id": "status"})
    return res["state"] if res else False

# 2. Warning System (Check/Set/Delete)
async def is_warned_in_db(user_id):
    res = await warns_col.find_one({"user_id": user_id})
    return True if res else False

async def set_warned_in_db(user_id):
    await warns_col.update_one({"user_id": user_id}, {"$set": {"warned": True}}, upsert=True)

async def delete_warned_user(user_id):
    await warns_col.delete_one({"user_id": user_id})

# 3. Approval System (.approve/.disapprove)
async def approve_user(user_id):
    await approved_col.update_one({"user_id": user_id}, {"$set": {"user_id": user_id}}, upsert=True)

async def disapprove_user(user_id):
    await approved_col.delete_one({"user_id": user_id})

async def is_approved(user_id):
    res = await approved_col.find_one({"user_id": user_id})
    return True if res else False
                              
