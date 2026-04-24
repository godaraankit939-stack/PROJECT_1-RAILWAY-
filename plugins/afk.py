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
MSG_COUNT = 0 # Messages count karne ke liye

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
        global AFK_STATUS, AFK_REASON, AFK_TIME, MSG_COUNT
        
        if event.is_private and event.chat_id == OWNER_ID and event.sender_id != OWNER_ID:
            aura_list = get_remote_aura()
            selected_aura = random.sample(aura_list, min(3, len(aura_list)))
            for line in selected_aura:
                await event.edit(line)
                await asyncio.sleep(1.5)
            return

        if not event.out:
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
            
            # Manual Off Stats
            now = datetime.datetime.now()
            diff = now - AFK_TIME
            hours, remainder = divmod(int(diff.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            t_str = f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m {seconds}s"
            
            stats_msg = (
                "**⌬ 𝖡𝖠𝖢𝖪 𝖨𝖳 𝖳𝖧𝖤 𝖦𝖧𝖮𝖲𝖳 𝖲𝖸𝖲𝖳𝖤𝖬** ⚡\n"
                f"◈ **𝖣𝗎𝗋𝖺𝗍𝗂𝗈𝗇:** `{t_str}`\n"
                f"◈ **𝖬𝖾𝗌𝗌𝖺𝗀𝖾𝗌:** `{MSG_COUNT}`"
            )
            AFK_STATUS = False
            MSG_COUNT = 0
            return await event.edit(stats_msg)

        # Set AFK
        AFK_STATUS = True
        MSG_COUNT = 0
        AFK_TIME = datetime.datetime.now()
        AFK_REASON = cmd_input if cmd_input else "I am the master of my own silence."
        
        await event.edit(f"**⌬ 𝖲𝖸𝖲𝖳𝖤𝖬 𝖨𝖲 𝖴𝖭𝖱𝖤𝖠𝖧𝖠𝖡𝖫𝖤** 💀\n`Ghost Mode Activated.`")

    # --- AUTO-OFF LOGIC ---
    @client.on(events.NewMessage(outgoing=True))
    async def auto_off_handler(event):
        global AFK_STATUS, AFK_TIME, MSG_COUNT
        if AFK_STATUS and not event.text.startswith(".afk"):
            now = datetime.datetime.now()
            diff = now - AFK_TIME
            hours, remainder = divmod(int(diff.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            t_str = f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m {seconds}s"
            
            back_msg = await event.respond(
                "**⌬ 𝖠𝖥𝖪 𝖠𝖴𝖳𝖮-𝖮𝖥▵**\n"
                f"◈ **𝖣𝗎𝗋𝖺𝗍𝗂𝗈𝗇:** `{t_str}`\n"
                f"◈ **𝖬𝖾𝗌𝗌𝖺𝗀𝖾𝗌:** `{MSG_COUNT}`\n"
                "`Welcome back, Master!`"
            )
            AFK_STATUS = False
            MSG_COUNT = 0
            await asyncio.sleep(5)
            await back_msg.delete()

    # --- REPLY LOGIC & COUNTER ---
    @client.on(events.NewMessage(incoming=True))
    async def reply_handler(event):
        global AFK_STATUS, AFK_REASON, AFK_TIME, MSG_COUNT
        
        if not AFK_STATUS:
            return

        me = await event.client.get_me()
        if event.sender_id == me.id or (event.sender and event.sender.bot):
            return

        if event.is_private or event.mentioned:
            if await is_banned(event.sender_id):
                return
            
            MSG_COUNT += 1 # Message count badhao
            
            now = datetime.datetime.now()
            diff = now - AFK_TIME
            hours, remainder = divmod(int(diff.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            time_str = f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m {seconds}s"

            response = (
                "**⌬ 𝖲𝖸𝖲𝖳𝖤𝖬 𝖨𝖲 𝖴𝖭𝖱𝖤𝖠𝖧𝖠𝖡𝖫𝖤** 💀\n\n"
                f"◈ **𝖲𝗍𝖺𝗍𝗎𝗌:** `𝖦𝗁𝗈𝗌𝗍 𝖬𝗈𝖽𝖾`\n"
                f"◈ **𝖱𝖾𝖺𝗌𝗈𝗇:** `{AFK_REASON}`\n"
                f"◈ **𝖲𝗂𝗇𝖼𝖾:** `{time_str}`\n\n"
                "`Don't disturb the silence.`"
            )
            await event.reply(response)
            
