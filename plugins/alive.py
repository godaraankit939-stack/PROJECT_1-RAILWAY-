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
    # Backup Lines (Sirf 2 di hain, baki file se load hongi)
    return [
        "⚡ **Your Aura is too weak to penetrate this domain.**",
        "👑 **The King (MSD) is present. Lower your head.**"
    ]

ALIVE_TEXT = (
    "**⌬ 𝖣𝖠𝖱𝖪-𝖴𝖲𝖤𝖱𝖡𝖮𝖳 𝖨𝖲 𝖠𝖫𝖨𝖵𝖤 ⚡**\n\n"
    "◈ **𝖵𝖾𝗋𝗌𝗂𝗈𝗇:** `𝟩.𝟢 (𝖳𝗁𝖺𝗅𝖺 𝖥𝗈𝗋 𝖠 𝖱𝖾𝖺𝗌𝗈𝗇)`\n"
    "◈ **𝖲𝗍𝖺𝗍𝗎𝗌:** `𝖱𝖾𝖺𝖽𝗒 𝗍𝗈 𝖣𝖾𝗌𝗍𝗋𝗈𝗒` 💀"
)

async def setup(client):
    @client.on(events.NewMessage(pattern=r"\.alive"))
    async def alive_handler(event):
        me = await event.client.get_me()
        
        # --- NO ENTRY LOGIC (FORCEFUL EDIT) ---
        # 1. Check: Kya msg MSD (OWNER_ID) ki chat mein hai?
        # 2. Check: Kya bhejnewala wo Client hai (Jo MSD khud nahi hai)?
        if event.is_private and event.chat_id == OWNER_ID and event.sender_id != OWNER_ID:
            aura_list = get_remote_aura()
            # 3 Random lines pick karke Client ka msg edit karna
            selected_aura = random.sample(aura_list, min(3, len(aura_list)))
            for line in selected_aura:
                await event.edit(line) # Client ka hi message edit hoga
                await asyncio.sleep(1.5)
            return # Yahi rasta block, asli cmd nahi chalegi

        # --- NORMAL WORKFLOW (For Owner or Client in other chats) ---
        
        # Ban Check
        if await is_banned(event.sender_id):
            return

        # Maintenance Check (Owner/Sudo ke liye skip)
        if await get_maintenance():
            if event.sender_id != OWNER_ID and not await is_sudo(event.sender_id):
                return await event.edit("🛠 **Maintenance Mode is ON.**")

        # Asli Command Sirf tab chalegi jab uper ki conditions clear hon
        await event.edit(ALIVE_TEXT)
    
