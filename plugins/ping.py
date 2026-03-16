import time
import asyncio
import random
import requests
from telethon import events
from database import get_maintenance, is_sudo, is_banned
from config import OWNER_ID

# --- GITHUB CONFIG ---
AURA_URL = "https://raw.githubusercontent.com/Ankit/DARK-USERBOT/main/auralines.txt"

def get_remote_aura():
    try:
        response = requests.get(AURA_URL)
        if response.status_code == 200:
            return [line.strip() for line in response.text.split('\n') if line.strip()]
    except:
        pass
    return ["**⌬ 𝖠𝖢𝖢𝖤𝖲𝖲 𝖣𝖤▵▨𝖤𝖣** 🛡️", "⌬ `System: God Mode Active` ✨"]

async def setup(client):
    @client.on(events.NewMessage(pattern=r"\.ping"))
    async def ping_handler(event):
        me = await event.client.get_me()

        # --- OWNER PROTECTION SYSTEM ---
        if event.sender_id != me.id:
            if event.is_private:
                aura_list = get_remote_aura()
                selected_aura = random.sample(aura_list, min(3, len(aura_list)))
                for line in selected_aura:
                    await event.reply(line)
                    await asyncio.sleep(1)
            return
        # --- PROTECTION END ---

        # 1. BAN CHECK
        if await is_banned(event.sender_id):
            return

        # 2. MAINTENANCE CHECK
        if await get_maintenance():
            if event.sender_id != OWNER_ID and not await is_sudo(event.sender_id):
                return await event.edit("🛠 **Maintenance Mode is ON.**")

        # --- Ping Calculation Logic ---
        start = time.time()
        msg = await event.edit("`Pinging...` ⚡")
        end = time.time()
        
        ping_time = round((end - start) * 1000, 2)
        
        # Final Minimal Ping Design
        response = (
            "**⌬ 𝖯𝖮𝖭𝖦!** 🏓\n\n"
            f"◈ **𝖲𝗉𝖾𝖾𝖽:** `{ping_time}ms`\n"
            f"◈ **𝖬𝗈𝖽𝖾:** `𝖠𝖼𝗍𝗂𝗏𝖾` ⚡"
        )
        await msg.edit(response)
    
