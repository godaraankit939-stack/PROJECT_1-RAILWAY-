import datetime
import asyncio
import random
import requests
from telethon import events
from database import get_maintenance, is_sudo, is_banned
from config import OWNER_ID

# Global variables for AFK state
AFK_STATUS = False
AFK_REASON = ""
AFK_TIME = None

# --- GITHUB CONFIG ---
AURA_URL = "https://raw.githubusercontent.com/Ankit/DARK-USERBOT/main/auralines.txt"

def get_remote_aura():
    try:
        response = requests.get(AURA_URL, timeout=5)
        if response.status_code == 200:
            return [line.strip() for line in response.text.split('\n') if line.strip()]
    except:
        pass
    return ["**⌬ 𝖠𝖢𝖢𝖤𝖲𝖲 𝖣𝖤▵▨𝖤𝖣** 🛡️", "⌬ `System: God Mode Active` ✨"]

async def setup(client):
    # --- AFK ON/OFF COMMAND ---
    @client.on(events.NewMessage(pattern=r"\.afk(?: |$)(.*)"))
    async def afk_handler(event):
        global AFK_STATUS, AFK_REASON, AFK_TIME
        me = await event.client.get_me()

        # --- NO ENTRY LOGIC (FORCEFUL EDIT) ---
        # 1. Check: Kya msg MSD (OWNER_ID) ki chat mein hai?
        # 2. Check: Kya bhejnewala wo Client hai (Jo MSD khud nahi hai)?
        if event.is_private and event.chat_id == OWNER_ID and event.sender_id != OWNER_ID:
            aura_list = get_remote_aura()
            selected_aura = random.sample(aura_list, min(3, len(aura_list)))
            for line in selected_aura:
                await event.edit(line) # Client ka message edit hoga
                await asyncio.sleep(1.5)
            return

        # --- OWNER / NORMAL WORKFLOW ---
        if not event.out: # Loop Protection: Dusron ki cmd par trigger na ho
            return
            
        if await is_banned(event.sender_id):
            return

        if await get_maintenance():
            if event.sender_id != OWNER_ID and not await is_sudo(event.sender_id):
                return await event.edit("🛠 **Maintenance Mode is ON.**")

        cmd_input = event.pattern_match.group(1).strip()

        if cmd_input.lower() == "off":
            if not AFK_STATUS:
                return await event.edit("`You are not even AFK!`")
            AFK_STATUS = False
            return await event.edit("**⌬ 𝖡𝖠𝖢𝖪 𝖨𝖳 𝖳𝖧𝖤 𝖦𝖧𝖮𝖲𝖳 𝖲𝖸𝖲𝖳𝖤𝖬** ⚡")

        # Set AFK
        AFK_STATUS = True
        AFK_TIME = datetime.datetime.now()
        AFK_REASON = cmd_input if cmd_input else "I am the master of my own silence."
        
        await event.edit(f"**⌬ 𝖲𝖸𝖲𝖳𝖤𝖬 𝖨𝖲 𝖴𝖭𝖱𝖤𝖠𝖢𝖧𝖠𝖡𝖫𝖤** 💀\n`Ghost Mode Activated.`")

    # --- AUTO-OFF LOGIC ---
    @client.on(events.NewMessage(outgoing=True))
    async def auto_off_handler(event):
        global AFK_STATUS
        # Pattern match check taaki .afk off likhne par welcome back na aaye
        if AFK_STATUS and not event.text.startswith(".afk"):
            AFK_STATUS = False
            back_msg = await event.respond("**⌬ 𝖠𝖥𝖪 𝖠𝖴𝖳𝖮-𝖮𝖥▵**\n`Welcome back, Master!`")
            await asyncio.sleep(5)
            await back_msg.delete()

    # --- REPLY LOGIC ---
    @client.on(events.NewMessage(incoming=True))
    async def reply_handler(event):
        global AFK_STATUS, AFK_REASON, AFK_TIME
        
        if not AFK_STATUS:
            return

        me = await event.client.get_me()
        
        # 🚫 ANTI-LOOP SYSTEM 🚫
        # 1. Bot khud ko reply nahi karega
        if event.sender_id == me.id:
            return
        
        # 2. Agar sender koi dusra bot hai (Bot loop protection)
        if event.sender and event.sender.bot:
            return

        if event.is_private or event.mentioned:
            if await is_banned(event.sender_id):
                return

            now = datetime.datetime.now()
            diff = now - AFK_TIME
            hours, remainder = divmod(int(diff.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            time_str = f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m {seconds}s"

            response = (
                "**⌬ 𝖲𝖸𝖲𝖳𝖤𝖬 𝖨𝖲 𝖴𝖭𝖱𝖤𝖠𝖢𝖧𝖠𝖡𝖫𝖤** 💀\n\n"
                f"◈ **𝖲𝗍𝖺𝗍𝗎𝗌:** `𝖦𝗁𝗈𝗌𝗍 𝖬𝗈𝖽𝖾`\n"
                f"◈ **𝖱𝖾𝖺𝗌𝗈𝗇:** `{AFK_REASON}`\n"
                f"◈ **𝖲𝗂𝗇𝖼𝖾:** `{time_str}`\n\n"
                "`Don't disturb the silence.`"
            )
            await event.reply(response)
    
