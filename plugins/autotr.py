import asyncio
from telethon import events
from database import get_maintenance, is_banned, is_sudo
from config import OWNER_ID

# --- SAFE IMPORT ---
try:
    from deep_translator import GoogleTranslator
    HAS_TR = True
except ImportError:
    HAS_TR = False

# --- GLOBAL SETTINGS ---
AUTO_TR_USERS = {}

# ================= 1. .autotr [lang] =================
@events.register(events.NewMessage(pattern=r"\.autotr(?: (.*))?"))
async def autotr_toggle(event):
    # 🛡️ NO-ENTRY
    if event.chat_id == OWNER_ID and event.sender_id != OWNER_ID:
        await event.edit("**⌬ 𝖠𝖢𝖢𝖤𝖲𝖲 𝖣𝖤▵▨𝖤▣** 🛡️")
        return

    # 🚫 BAN LOGIC
    if await is_banned(event.sender_id):
        await event.edit("`YOU WERE BANNED BY OWNER!`")
        return

    if not HAS_TR:
        return await event.edit("`❌ Error: requirements.txt mein 'deep-translator' add karke Render pe redeploy karo!`")

    user_id = event.sender_id
    input_lang = event.pattern_match.group(1)

    if user_id in AUTO_TR_USERS and not input_lang:
        del AUTO_TR_USERS[user_id]
        await event.edit("🔄 **Auto-Translate Mode: OFF**")
        await asyncio.sleep(2)
        return await event.delete()

    if not input_lang:
        return await event.edit("`❌ Language code dalo! Example: .autotr hi`")

    AUTO_TR_USERS[user_id] = input_lang.strip()
    await event.edit(f"🚀 **Auto-Translate ACTIVE: [{input_lang.upper()}]**")
    await asyncio.sleep(2)
    await event.delete()

# ================= 2. THE GHOST WORKER =================
@events.register(events.NewMessage(outgoing=True))
async def translator_worker(event):
    user_id = event.sender_id
    if not HAS_TR or user_id not in AUTO_TR_USERS or event.text.startswith("."):
        return

    try:
        translated = GoogleTranslator(source='auto', target=AUTO_TR_USERS[user_id]).translate(event.text)
        if translated.strip().lower() != event.text.strip().lower():
            await event.edit(translated)
    except:
        pass

async def setup(client):
    client.add_event_handler(autotr_toggle)
    client.add_event_handler(translator_worker)
    
