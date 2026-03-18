import asyncio
import random
import requests
from telethon import events
from database import get_maintenance, is_sudo, is_banned
from config import OWNER_ID

# --- GITHUB CONFIG (Aura Lines) ---
AURA_URL = "https://raw.githubusercontent.com/Ankit/DARK-USERBOT/main/auralines.txt"

def get_remote_aura():
    try:
        response = requests.get(AURA_URL, timeout=5)
        if response.status_code == 200:
            return [line.strip() for line in response.text.split('\n') if line.strip()]
    except:
        pass
    return ["**⌬ 𝖠𝖢𝖢𝖤𝖲𝖲 𝖣𝖤▵▨𝖤▣** 🛡️", "⌬ `System: God Mode Active` ✨"]

# --- UPDATED HELP MENU (Google -> Ask) ---
HELP_MENU = """
┏━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃     ⌬ DARK X USERBOT ⌬       ┃
┣━━━━━━━━━━━━┳━━━━━━━━━━━━━┫
┃ ◈ Afk        ┃ ◈ Animate     ┃
┃ ◈ Antipm     ┃ ◈ B-Cast      ┃
┃ ◈ Clone      ┃ ◈ Create      ┃
┃ ◈ Destruct   ┃ ◈ Dict        ┃
┃ ◈ Ask        ┃ ◈ Info        ┃
┃ ◈ Lyrics     ┃ ◈ Memify      ┃
┃ ◈ Mention    ┃ ◈ Ping        ┃
┃ ◈ Quote      ┃ ◈ Raid/Rraid  ┃
┃ ◈ Tiny       ┃ ◈ Trans       ┃
┃ ◈ Weather    ┃ ◈ Magic       ┃
┣━━━━━━━━━━━━┻━━━━━━━━━━━━━┫
┃      ┃┃ Powered By : MSD 👑 ┃┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━┛
"""

# ================= MAIN HANDLER =================
async def setup(client):
    @client.on(events.NewMessage(outgoing=True, pattern=r"\.help(?: |$)(.*)"))
    async def help_handler(event):
        # 🛡️ 1. NO ENTRY LOGIC (TERA REAL PROTECTION)
        if event.is_private and event.chat_id == OWNER_ID and event.sender_id != OWNER_ID:
            aura_list = get_remote_aura()
            selected_aura = random.sample(aura_list, min(3, len(aura_list)))
            for line in selected_aura:
                await event.edit(line)
                await asyncio.sleep(1.5)
            return

        # 🚫 2. BAN LOGIC
        if await is_banned(event.sender_id):
            return await event.edit("`YOU WERE BANNED BY OWNER!`")

        # 🛠️ 3. MAINTENANCE LOGIC
        if await get_maintenance() and event.sender_id != OWNER_ID and not await is_sudo(event.sender_id):
            return await event.edit("🛠 **System Status: Maintenance Mode.**")

        cmd = event.pattern_match.group(1).lower().strip()
        
        if not cmd:
            # Main Menu with Custom Instruction Line
            final_help = f"```\n{HELP_MENU}\n```"
            final_help += "\n**💡 Usage:** `.help <cmd_name>` to unleash the power!"
            await event.edit(final_help)
        else:
            # Specific command work logic (Clean & Simple)
            # Yahan tu baad mein PLUGINS_HELP logic add kar sakta hai
            await event.edit(f"✨ **Usage of `{cmd.upper()}`** will be shown here soon.")
            await asyncio.sleep(3)
            await event.delete()

# ================================================
