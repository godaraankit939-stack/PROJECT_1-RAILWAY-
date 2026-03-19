import asyncio
import random
import requests
from telethon import events
from database import get_maintenance, is_sudo, is_banned
from config import OWNER_ID
# DARK folder ke pdata.py se HOT list import kar rahe hain
from DARK.pdata import HOT

# --- GITHUB CONFIG (Aura Lines for No Entry) ---
AURA_URL = "https://raw.githubusercontent.com/Ankit/DARK-USERBOT/main/auralines.txt"

def get_remote_aura():
    try:
        response = requests.get(AURA_URL, timeout=5)
        if response.status_code == 200:
            return [line.strip() for line in response.text.split('\n') if line.strip()]
    except:
        pass
    return ["**⌬ 𝖠𝖢𝖢𝖤𝖲𝖲 𝖣𝖤▵▨𝖤▣** 🛡️", "⌬ `System: God Mode Active` ✨"]

# ================= MAIN HANDLER =================
async def setup(client):
    @client.on(events.NewMessage(pattern=r"^\.hot$"))
    async def hot_handler(event):
        # 🛡️ 1. NO ENTRY LOGIC (Security for Owner's DM)
        if event.is_private and event.chat_id == OWNER_ID and event.sender_id != OWNER_ID:
            aura_list = get_remote_aura()
            selected_aura = random.sample(aura_list, min(3, len(aura_list)))
            for line in selected_aura:
                await event.edit(line)
                await asyncio.sleep(1.5)
            return

        # 🚫 2. BAN LOGIC (Owner Exempted)
        if event.sender_id != OWNER_ID and await is_banned(event.sender_id):
            try:
                return await event.reply("`YOU WERE BANNED BY OWNER!`")
            except:
                return

        # 🛠️ 3. MAINTENANCE LOGIC
        if await get_maintenance() and event.sender_id != OWNER_ID and not await is_sudo(event.sender_id):
            return await event.edit("🛠 **System Status: Maintenance Mode.**")

        # ✅ 4. RANDOM PICK LOGIC
        # HOT list se random link uthayega
        random_content = random.choice(HOT)
        
        try:
            # Seedha link bhej dega (Telegram ise preview mein video/photo bana dega)
            await event.edit(f"{random_content}")
        except Exception as e:
            # Backup agar edit fail ho jaye
            await event.reply(f"{random_content}")

# ================================================
