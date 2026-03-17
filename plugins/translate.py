import asyncio
import random
import requests
import urllib.parse
from telethon import events
from database import get_maintenance, is_sudo, is_banned
from config import OWNER_ID

# --- CONFIG (Remote Aura) ---
AURA_URL = "https://raw.githubusercontent.com/Ankit/DARK-USERBOT/main/auralines.txt"

def get_remote_aura():
    try:
        response = requests.get(AURA_URL, timeout=5)
        if response.status_code == 200:
            return [line.strip() for line in response.text.split('\n') if line.strip()]
    except Exception:
        pass
    return ["**⌬ 𝖠𝖢𝖢𝖤𝖲𝖲 𝖣𝖤▵▨𝖤𝖣** 🛡️"]

# ================= TRANSLATE CMD (NO-CGI LOGIC) =================
@events.register(events.NewMessage(pattern=r"\.tr ?([a-z]{2})? ?(.*)"))
async def translate_cmd(event):
    # 🛡️ 1. NO ENTRY LOGIC (Exact working logic you liked)
    if event.is_private and event.chat_id == OWNER_ID and event.sender_id != OWNER_ID:
        aura_list = get_remote_aura()
        selected_aura = random.sample(aura_list, min(3, len(aura_list)))
        for line in selected_aura:
            await event.edit(line)
            await asyncio.sleep(1.5) # Forceful 5s delay
        return

    # 🛠️ 2. BAN & MAINTENANCE CHECK
    if await is_banned(event.sender_id):
        return
    if await get_maintenance() and event.sender_id != OWNER_ID and not await is_sudo(event.sender_id):
        return await event.edit("`System Status: Maintenance Mode Active.`")

    # 🛠️ 3. TEXT EXTRACTION
    dest_lang = event.pattern_match.group(1) or "hi"
    input_str = event.pattern_match.group(2).strip()
    reply = await event.get_reply_message()

    if not input_str and reply:
        text_to_tr = reply.text
    elif input_str:
        text_to_tr = input_str
    else:
        return await event.edit("`Error: Provide text or reply to a message!`")

    await event.edit(f"`🔠 Translating to {dest_lang.upper()}...`")

    try:
        # 🚀 NO-LIBRARY LOGIC: Using direct Google API endpoint
        # Hum urllib use kar rahe hain jo 'cgi' ka modern replacement hai
        encoded_text = urllib.parse.quote(text_to_tr)
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={dest_lang}&dt=t&q={encoded_text}"
        
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=10).json()
        
        # Google returns a nested list, we join the translated parts
        translated_text = "".join([part[0] for part in res[0] if part[0]])

        # 📋 Clean Output
        final_msg = (
            f"📥 **Input:** `{text_to_tr[:50]}...`\n"
            f"📤 **Output ({dest_lang.upper()}):**\n`{translated_text}`\n\n"
            f"**DARK-USERBOT** 💀"
        )
        await event.edit(final_msg)

    except Exception as e:
        await event.edit(f"❌ `Translation Error: {str(e)}`")

# ================= SETUP =================
async def setup(client):
    client.add_event_handler(translate_cmd)
        
