import asyncio
import random
import requests
from telethon import events
from googletrans import Translator
from database import get_maintenance, is_sudo, is_banned
from config import OWNER_ID

AURA_URL = "https://raw.githubusercontent.com/Ankit/DARK-USERBOT/main/auralines.txt"

def get_remote_aura():
    try:
        res = requests.get(AURA_URL, timeout=5)
        if res.status_code == 200: return [l.strip() for l in res.text.split('\n') if l.strip()]
    except: pass
    return ["**⌬ 𝖠𝖢𝖢𝖤𝖲𝖲 𝖣𝖤▵▨𝖤𝖣** 🛡️"]

@events.register(events.NewMessage(pattern=r"\.tr ?([a-z]{2})? ?(.*)"))
async def tr_cmd(event):
    # 🛡️ NO ENTRY
    if event.is_private and event.chat_id == OWNER_ID and event.sender_id != OWNER_ID:
        aura = get_remote_aura()
        for line in random.sample(aura, min(3, len(aura))):
            await event.edit(line); await asyncio.sleep(1.5)
        return

    if await is_banned(event.sender_id): return
    if await get_maintenance() and event.sender_id != OWNER_ID: return

    # Logic for language and text
    lang = event.pattern_match.group(1) or "hi" # Default to Hindi
    text = event.pattern_match.group(2).strip()
    reply = await event.get_reply_message()

    if not text and reply:
        text = reply.text
    
    if not text:
        return await event.edit("`Error: Kuch toh likho translate karne ke liye!`")

    await event.edit("`🔠 Translating...`")

    try:
        translator = Translator()
        translated = translator.translate(text, dest=lang)
        
        # Clean Result
        res = (
            f"📥 **Input:** `{text[:50]}...`\n"
            f"📤 **Output ({lang}):**\n`{translated.text}`\n\n"
            f"💀 **DARK-USERBOT**"
        )
        await event.edit(res)
    except Exception as e:
        await event.edit(f"❌ `Translation Error: {str(e)}`")

async def setup(client):
    client.add_event_handler(tr_cmd)
  
